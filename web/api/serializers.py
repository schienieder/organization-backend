from rest_framework import serializers
from django.utils.safestring import mark_safe
import secrets
from api.models import User, UserAuth
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
        model = User
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
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
            "is_active": {"read_only": True},
        }

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            is_teacher=validated_data["is_teacher"],
            is_verified=validated_data["is_verified"],
        )

        user.set_password(validated_data["password"])
        user.save()

        milliseconds = 24 * 60 * 60 * 1000

        auth = UserAuth.objects.create(
            one_time_code=secrets.token_hex(6), expiration=milliseconds, owner=user.id
        )

        auth.save()

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

    user = serializers.RelatedField(source="user", read_only=False)

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

        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):

        userInfo = UserInfo.objects.create(
            year_level=validated_data["year_level"],
            course=validated_data["course"],
            section=validated_data["section"],
            student_id=validated_data["student_id"],
            date_of_birth=validated_data["date_of_birth"],
            age=validated_data["age"],
            profile_image=validated_data["profile_image"],
            background_image=validated_data["background_image"],
            read_me=validated_data["read_me"],
            user=User.objects.get(pk=validated_data["user"]),
        )

        userInfo.save()

        return userInfo

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class OrgApplicationSerializer(serializers.ModelSerializer):

    owner = serializers.RelatedField(source="owner", read_only=False)

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
            owner=pk=validated_data["user"]
        )

        orgApp.save()

        return orgApp

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class OrgSerializer(serializers.ModelSerializer):

    owner = serializers.RelatedField(source="owner", read_only=False)

    class Meta:
        model = OrgApplication
        fields = [
            "id",
            "create_restricted",
            "create_blocked",
            "org_max_count",
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

    def create(self, validated_data):

        orgMake = OrgApplication.objects.create(
            create_restricted=validated_data["create_restricted"],
            create_blocked=validated_data["create_blocked"],
            org_max_count=validated_data["org_max_count"],
            logo=validated_data["logo"],
            background_image=validated_data["background_image"],
            verified=validated_data["verified"],
            readme=validated_data["readme"],
            contact_number=validated_data["contact_number"],
            email=validated_data["email"],
            password=validated_data["password"],
            member_limit=validated_data["member_limit"],
            restricted=validated_data["restricted"],
            disabled=validated_data["disabled"],
            restriction_type=validated_data["restriction_type"],
            owner=User.objects.get(pk=validated_data["user"]),
        )

        orgMake.save()

        return orgMake

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class VotesSerializer(serializers.ModelSerializer):

    owner = serializers.RelatedField(source="owner", read_only=False)

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
            owner=User.objects.get(pk=validated_data["user"]),
        )

        votesMaker.save()

        return votesMaker

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class PollCandidateSerializer(serializers.ModelSerializer):

    user = serializers.RelatedField(source="user", read_only=False)

    class Meta:
        model = PollCandidate
        fields = [
            "id",
            "position",
            "partylist",
            "is_disqualified",
            "is_winner",
            "date_created",
            "user"
        ]

        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):

        pollMaker = PollCandidate.objects.create(
            position=validated_data["position"],
            partylist=validated_data["partylist"],
            is_disqualified=validated_data["is_disqualified"],
            is_winner=validated_data["is_winner"],
            date_created=validated_data["date_created"],
            user=User.objects.get(pk=validated_data["user"]),
        )

        pollMaker.save()

        return pollMaker

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class MainPollSerializer(serializers.ModelSerializer):

    owner = serializers.RelatedField(source="owner", read_only=False)
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
            owner=User.objects.get(pk=validated_data["owner"]),
        )

        pollMaker.save()

        return pollMaker

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class AttendanceSerializer(serializers.ModelSerializer):

    owner = serializers.RelatedField(source="owner", read_only=False)

    class Meta:
        model = Attendance
        fields = ["id", "date", "time", "ip_address", "owner"]

        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):

        attendanceMaker = Attendance.objects.create(
            date=validated_data["date"],
            time=validated_data["time"],
            ip_address=validated_data["ip_address"],
            owner=User.objects.get(pk=validated_data["owner"])
        )

        attendanceMaker.save()

        return attendanceMaker

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class EventSerializer(serializers.ModelSerializer):

    org = serializers.RelatedField(source="org")
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
            org=Org.objects.get(pk=validated_data["org"])
        )

        EventMaker.save()

        return EventMaker

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class ReplySerializer(serializers.ModelSerializer):

    user = serializers.RelatedField(source="user")
    reply_replies = ReplySerializer(read_only=True, many=True)

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
            user=User.objects.get(pk=validated_data["owner"]),
        )

        replyMaker.save()

        return replyMaker

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class PostSerializer(serializers.ModelSerializer):

    user = serializers.RelatedField(source="user")

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
            user=User.objects.get(pk=validated_data["user"]),
            org=Org.objects.get(pk=validated_data["org"])
        )

        postMaker.save()

        return postMaker

    def update(self, instance, validated_data):

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance