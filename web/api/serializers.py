from rest_framework import serializers
from django.utils.safestring import mark_safe
import secrets
from api.models import MyUser, UserAuth
from api.models import UserInfo
from api.models import Badges
from api.models import OrgApplication
from api.models import Org
from api.models import Votes
from api.models import PollCandidate
from api.models import MainPoll
from api.models import Attendance
from api.models import Event
from api.models import Reply
from api.models import Post
from api.models import Code
from api.models import UserOrg
from datetime import datetime, timedelta
import datetime
import uuid


# from api.validators import GroupCreatePermission


class BadgesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badges
        fields = ["id", "condition", "name", "date_received"]

        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):

        badges = Badges.objects.create(
            condition=validated_data["condition"],
            name=validated_data["name"],
            date_received=validated_data["date_received"],
        )

        badges.save()

        return badges

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class UserSerializer(serializers.ModelSerializer):

    badges = BadgesSerializer(read_only=True, many=True)

    class Meta:
        model = MyUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_active",
            "is_verified",
            "is_teacher",
            "badges",
            "user_info",
            "user_org_control",
            "user_code",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
            "is_active": {"read_only": True},
            "user_info": {"read_only": True},
            "user_org_control": {"read_only": True},
            "user_code": {"read_only": True},
        }

    def create(self, validated_data):

        user = MyUser.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            is_teacher=validated_data["is_teacher"],
            is_verified=validated_data["is_verified"],
        )

        user.set_password(validated_data["password"])
        user.save()

        auth = UserAuth.objects.create(
            one_time_code=secrets.token_hex(6),
            expiration=datetime.timedelta(days=1),
            owner=user,
        )

        auth.save()

        userInfo = UserInfo.objects.create(user=user)
        userInfo.save()

        userCode = Code.objects.create(code=uuid.uuid4, user=user)
        userCode.save()

        userOrg = UserOrg.objects.create(owner=user)
        userOrg.save()

        return user

    def update(self, instance, validated_data):

        password = validated_data.pop("password", None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = [
            "id",
            "year_level",
            "course",
            "section",
            "student_id",
            "date_of_birth",
            "age",
            "profile_image",
            "background_image",
            "read_me",
            "user",
        ]

        extra_kwargs = {"id": {"read_only": True}, "user": {"read_only": True}}

    def update(self, instance, validated_data):
        info = UserInfo.objects.get(user=instance)

        for (key, value) in validated_data.items():
            setattr(info, key, value)

        info.save()

        return info


class OrgApplicationSerializer(serializers.ModelSerializer):

    owner = serializers.RelatedField(source="owner", read_only=True)

    class Meta:
        model = OrgApplication
        fields = [
            "id",
            "date_created",
            "flagged",
            "is_accepted",
            "decline_reason",
            "date_accepted",
            "owner",
        ]

        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):

        orgApp = OrgApplication.objects.create(
            date_created=validated_data["date_created"],
            flagged=validated_data["flagged"],
            is_accepted=validated_data["is_accepted"],
            decline_reason=validated_data["decline_reason"],
            date_accepted=validated_data["date_accepted"],
            owner=validated_data["user"],
        )

        orgApp.save()

        return orgApp

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = [
            "id",
            "name",
            "date_created",
            "description",
            "logo",
            "background_image",
            "verified",
            "readme",
            "contact_number",
            "email",
            "official",
            "password",
            "member_limit",
            "restricted",
            "disabled",
            "restriction_type",
            "owner",
        ]

        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def validate_name(self, name):
        user_org_restrictions = UserOrg.objects.get(owner=self.context["request"].user)

        if user_org_restrictions.create_restricted is True:
            raise serializers.ValidationError(
                "Failed to create organization. User is Restricted"
            )

        if user_org_restrictions.create_blocked is True:
            raise serializers.ValidationError(
                "Failed to create organization. User is Restricted"
            )

        if (
            user_org_restrictions.org.all().count() + 1
            > user_org_restrictions.org_max_count
        ):
            raise serializers.ValidationError(
                "Failed to create organization. Org Limit Reached"
            )

    def create(self, validated_data):
        instance = Org.objects.create(owner=self.context["request"].user)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    def update(self, instance, validated_data):

        organization = Org.objects.get(pk=validated_data.id)

        for (key, value) in validated_data.items():
            setattr(organization, key, value)

        organization.save()

        return organization


class VotesSerializer(serializers.ModelSerializer):

    owner = serializers.RelatedField(source="owner", read_only=True)

    class Meta:
        model = Votes
        fields = [
            "id",
            "date_voted",
            "validated",
            "ip_address",
            "owner",
        ]

        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):

        votesMaker = Votes.objects.create(
            date_voted=validated_data["date_voted"],
            validated=validated_data["validated"],
            ip_address=validated_data["ip_address"],
            owner=MyUser.objects.get(pk=validated_data["user"]),
        )

        votesMaker.save()

        return votesMaker

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class PollCandidateSerializer(serializers.ModelSerializer):

    user = serializers.RelatedField(source="user", read_only=True)

    class Meta:
        model = PollCandidate
        fields = [
            "id",
            "position",
            "partylist",
            "is_disqualified",
            "is_winner",
            "date_created",
            "user",
        ]

        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):

        pollMaker = PollCandidate.objects.create(
            position=validated_data["position"],
            partylist=validated_data["partylist"],
            is_disqualified=validated_data["is_disqualified"],
            is_winner=validated_data["is_winner"],
            date_created=validated_data["date_created"],
            user=MyUser.objects.get(pk=validated_data["user"]),
        )

        pollMaker.save()

        return pollMaker

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class MainPollSerializer(serializers.ModelSerializer):

    owner = serializers.RelatedField(source="owner", read_only=True)
    candidates = PollCandidateSerializer(read_only=True, many=True)

    class Meta:
        model = MainPoll
        fields = [
            "id",
            "title",
            "description",
            "date_created",
            "is_open",
            "date_open",
            "date_close",
            "finished",
            "is_deleted",
            "notes",
            "conditions",
            "owner",
            "candidates",
        ]

        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):

        pollMaker = MainPoll.objects.create(
            title=validated_data["title"],
            description=validated_data["description"],
            date_created=validated_data["date_created"],
            is_open=validated_data["is_open"],
            date_open=validated_data["date_open"],
            date_close=validated_data["date_close"],
            finished=validated_data["finished"],
            is_deleted=validated_data["is_deleted"],
            notes=validated_data["notes"],
            conditions=validated_data["conditions"],
            org=Org.objects.get(pk=validated_data["org"]),
            owner=MyUser.objects.get(pk=validated_data["owner"]),
        )

        pollMaker.save()

        return pollMaker

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class AttendanceSerializer(serializers.ModelSerializer):

    owner = serializers.RelatedField(source="owner", read_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "date", "time", "ip_address", "owner"]

        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):

        attendanceMaker = Attendance.objects.create(
            date=validated_data["date"],
            time=validated_data["time"],
            ip_address=validated_data["ip_address"],
            owner=MyUser.objects.get(pk=validated_data["owner"]),
        )

        attendanceMaker.save()

        return attendanceMaker

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class EventSerializer(serializers.ModelSerializer):

    org = serializers.RelatedField(source="org", read_only=True)
    event_attendance = AttendanceSerializer(read_only=True, many=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "start_date",
            "end_date",
            "ended",
            "canceled",
            "started",
            "description",
            "org",
            "event_attendance",
        ]

        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):

        EventMaker = Event.objects.create(
            name=validated_data["name"],
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
            ended=validated_data["ended"],
            canceled=validated_data["canceled"],
            started=validated_data["started"],
            description=validated_data["description"],
            org=Org.objects.get(pk=validated_data["org"]),
        )

        EventMaker.save()

        return EventMaker

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class ReplySerializer(serializers.ModelSerializer):

    user = serializers.RelatedField(source="user", read_only=True)

    class Meta:
        model = Reply
        fields = ["id", "content", "date_replied", "hearts", "user", "reply_replies"]

        extra_kwargs = {"id": {"read_only": True}}

    def get_reply_replies(self):
        reply_replies = super(ReplySerializer, self).get_reply_replies()
        reply_replies["reply_replies"] = ReplySerializer(many=True)
        return reply_replies

    def create(self, validated_data):

        replyMaker = Event.objects.create(
            content=validated_data["content"],
            date_replied=validated_data["date_replied"],
            hearts=validated_data["hearts"],
            user=MyUser.objects.get(pk=validated_data["owner"]),
        )

        replyMaker.save()

        return replyMaker

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class PostSerializer(serializers.ModelSerializer):

    user = serializers.RelatedField(source="user", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "admin_only",
            "date_posted",
            "content",
            "is_pinned",
            "hearts",
            "views",
            "is_private",
            "user",
        ]

        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):

        postMaker = Post.objects.create(
            admin_only=validated_data["admin_only"],
            date_posted=validated_data["date_posted"],
            content=validated_data["content"],
            is_pinned=validated_data["is_pinned"],
            hearts=validated_data["hearts"],
            views=validated_data["views"],
            is_private=validated_data["is_private"],
            user=MyUser.objects.get(pk=validated_data["user"]),
            org=Org.objects.get(pk=validated_data["org"]),
        )

        postMaker.save()

        return postMaker

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance