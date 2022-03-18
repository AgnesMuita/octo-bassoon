from utils.observable import Observable, Observer
from abc import ABC, abstractmethod
from utils.feedback import Feedback
from students import models
from utils import utilityfunctions
import string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text


class IAccount(ABC):
    pass


class Account(IAccount, Observable):
    def __init__(self, request):
        self.feedback = Feedback()
        self.observers = []
        self.request = request
        self.account_info = None
        self.generated_info = None

    def contact_exists(self, contact_type, contact):
        try:
            existing_contact = models.Contact.objects.get(
                contact_type__exact=contact_type, contact__exact=contact)
        except(models.Contact.DoesNotExist):
            existing_contact = False
        return existing_contact

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        for i in range(self.observers):
            if self.observers[i] == observer:
                del self.observers[i]

    def notify(self):
        for obs in self.observers:
            obs.update(self)

    @property
    def status(self):
        current_fb = self.feedback.getfb()
        return self.feedback.get(status=current_fb["status"], data={"account_info": self.account_info, "generated_info": self.generated_info, "request": self.request})

    @abstractmethod
    def create(self, **account_info):
        pass

    @abstractmethod
    def remove(self, **account_info):
        pass


class UserAccount(Account):
    def __init__(self, request):
        Account.__init__(self, request)

    def create_activation_code(self, id, email):
        # let activation codes expire in 24 Hours
        expires = utilityfunctions.getTimestamp() + 86400
        email_code = utilityfunctions.generateToken(
            size=6, chars=string.digits)
        link_code = utilityfunctions.generateToken(size=50)
        uuid = urlsafe_base64_encode(force_bytes(id))
        new_code = models.ActivationCode(user=models.User(
            id=id), email=email, email_code=email_code, link_code=link_code, expires=expires, uuid=uuid)
        new_code.save()
        if not new_code.code_id:
            return self.feedback.get(status=Feedback.GENERAL_ERROR, message="Activation code could not be created!")
        return self.feedback.get(status=Feedback.SUCCESS, data=new_code)

    def get_user(self, id):
        try:
            user = models.User.objects.get(pk=id)
        except(models.User.DoesNotExist):
            user = None
        return user

    def save_contact_info(self, contacts):
        added_contacts = []
        for c in contacts:
            action = c["action"] if "action" in c else "add"
            if action == "add":
                contact_type = c.get("contact_type", None)
                contact_class = c.get("contact_class", "primary")
                contact = c.get("contact", None)
                owner_type = c.get("owner_type", None)
                owner_id = c.get("owner_id", None)
                if contact_type and contact and owner_type and owner_id:
                    existing_contact = self.contact_exists(
                        contact_type, contact)
                    if not existing_contact:
                        user_contact = models.Contact(contact_type=contact_type, contact_class=contact_class,
                                                      contact=contact, owner_type=owner_type, owner_id=owner_id)
                        user_contact.save()
                        added_contacts.append(user_contact)
            else:
                contact_id = c.get("contact_id", None)
                if contact_id:
                    try:
                        user_contact = models.Contact.objects.get(
                            pk=contact_id)
                        user_contact.deleted = 1
                        user_contact.save(update_fields=["deleted"])
                    except(models.Contact.DoesNotExist):
                        pass
        return self.feedback.get(status=Feedback.SUCCESS, data=added_contacts)

    def save_user(self, **user_info):
        action = user_info.get("action", "add")
        first_name = user_info.get("first_name", None)
        middle_name = user_info.get("middle_name", "")
        last_name = user_info.get("last_name", None)
        date_of_birth = user_info.get("date_of_birth", "")
        gender = user_info.get("gender", "unisex")
        user_group = user_info.get("user_group", [])
        user_photo = user_info.get("user_photo", None)
        if action == "add":
            tenant = user_info.get("tenant", None)
            user_name = user_info.get("email", None)
            password = user_info.get("password", None)
            if first_name and last_name and user_group and password and user_name:
                user = models.User(
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    date_of_birth=date_of_birth,
                    gender=gender,
                    user_name=user_name,
                    tenant=tenant,
                    user_photo=user_photo)
                user.set_password(password)
                user.save()
                if user.id:
                    return self.feedback.get(status=Feedback.GENERAL_ERROR, message="Could not create user!")

            else:
                return self.feedback.get(status=Feedback.GENERAL_ERROR, message="Provide all required user information: First Name, Last Name and User Group")
        else:
            user_id = user_info.get("user_id", None)
            update = []
            if user_id:
                try:
                    user = models.User.objects.get(pk=user_id)
                    if first_name:
                        user.first_name = first_name
                        update.append("first_name")
                    if middle_name:
                        user.middle_name = middle_name
                        update.append("middle_name")
                    if last_name:
                        user.last_name = last_name
                        update.append("last_name")
                    if date_of_birth:
                        user.date_of_birth = date_of_birth
                        update.append("date_of_birth")
                    if gender:
                        user.gender = gender
                        update.append("gender")
                    if user_group:
                        user.user_group = user_group
                        update.append("user_group")
                    if user_photo:
                        user.user_photo = user_photo
                        update.append("user_photo")
                    user.save(update_fields=update)
                    return self.feedback.get(status=Feedback.SUCCESS, data=user)
                except(models.User.DoesNotExist):
                    return self.feedback.get(status=Feedback.GENERAL_ERROR, message="User not found!")
            else:
                return self.feedback.get(status=Feedback.GENERAL_ERROR, message="User not specified!")

    def create(self, **account_info):
        # check that provided email address does not already exist.
        email_exists = self.contact_exists("email", account_info["email"])
        if email_exists:
            return self.feedback.get(status=Feedback.GENERAL_ERROR, message="Email address provided already exists!")
        self.generated_info = {
            "user_name": account_info["email"], "password": utilityfunctions.generateToken(size=8)}

        # create user:
        save_user_feedback = self.save_user(
            first_name=account_info["first_name"],
            middle_name=account_info.get("middle_name", ""),
            last_name=account_info["last_name"],
            date_of_birth=account_info.get("date_of_birth", ""),
            gender=account_info.get("gender", "unisex"),
            user_name=account_info["email"],
            user_group=account_info["user_group"],
            tenant=account_info["tenant"],
            user_photo=account_info.get("user_photo", None),
            password=self.generated_info['password'],
            email=account_info["email"],
        )
        if save_user_feedback["status"] != Feedback.SUCCESS:
            return save_user_feedback
        self.generated_info["user"] = save_user_feedback["data"]

        # create activation code.
        activation_code_feedback = self.create_activation_code(
            self.generated_info["user"].id, account_info["email"])
        if activation_code_feedback["status"] != Feedback.SUCCESS:
            return activation_code_feedback
        self.generated_info["code"] = activation_code_feedback["data"]

        # register user apps
        apps = account_info.get("apps", None)
        user_apps_feedback = self.register_apps(
            self.generated_info["user"].id, apps=apps)
        if user_apps_feedback["status"] == Feedback.SUCCESS:
            self.generated_info["apps"] = user_apps_feedback["data"]

        # save user contact info
        user_contact_feedback = self.save_contact_info([{
            "contact_type": "email",
            "contact_class": "primary",
            "contact": account_info["email"],
            "owner_type": "user",
            "owner_id": self.generated_info["user"].id,
            "action": "add"
        }])
        if user_contact_feedback["status"] == Feedback.SUCCESS:
            self.generated_info["contacts"] = user_contact_feedback["data"]
            self.notify()
        return self.feedback.get(status=Feedback.SUCCESS, data=self.generated_info)

    def remove(self, **account_info):
        pass

    def get_tenant_app_role_id(self, tenant_app, role_internal_name):
        app_role_id = None
        for r in tenant_app.app.app_roles.all():
            if r.role.role_internal_name == role_internal_name:
                app_role_id = r.id
        return app_role_id
