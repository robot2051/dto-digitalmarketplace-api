from __future__ import absolute_import

import os
import json
import pytest
from datetime import datetime, timedelta

from nose.tools import assert_equal, assert_in

from app import create_app, db
from app.models import Address, Service, Supplier, Framework, Lot, User, FrameworkLot, Brief, getUtcTimestamp

TEST_SUPPLIERS_COUNT = 3


COMPLETE_DIGITAL_SPECIALISTS_BRIEF = {
    "essentialRequirements": ["MS Paint", "GIMP"],
    "startDate": "31/12/2016",
    "evaluationType": ["Reference", "Interview"],
    "niceToHaveRequirements":  ["LISP"],
    "existingTeam": "Nice people.",
    "specialistWork": "All the things",
    "workingArrangements": "Just get the work done.",
    "organisation": "Org.org",
    "location": "Wales",
    "specialistRole": "developer",
    "title": "I need a Developer",
    "priceWeighting": 85,
    "contractLength": "3 weeks",
    "culturalWeighting": 5,
    "securityClearance": "Developed vetting required.",
    "technicalWeighting": 10,
    "culturalFitCriteria": ["CULTURAL", "FIT"],
    "numberOfSuppliers": 3,
    "summary": "Doing some stuff to help out.",
    "workplaceAddress": "Aviation House",
    "requirementsLength": "2 weeks"
}


class WSGIApplicationWithEnvironment(object):
    def __init__(self, app, **kwargs):
        self.app = app
        self.kwargs = kwargs

    def __call__(self, environ, start_response):
        for key, value in self.kwargs.items():
            environ[key] = value
        return self.app(environ, start_response)


class BaseApplicationTest(object):
    lots = {
        "iaas": "G6-IaaS.json",
        "saas": "G6-SaaS.json",
        "paas": "G6-PaaS.json",
        "scs": "G6-SCS.json"
    }

    config = None

    def setup(self):
        self.app = create_app('test')
        self.client = self.app.test_client()
        self.setup_authorization(self.app)

    def setup_authorization(self, app):
        """Set up bearer token and pass on all requests"""
        valid_token = 'valid-token'
        app.wsgi_app = WSGIApplicationWithEnvironment(
            app.wsgi_app,
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_token))
        self._auth_tokens = app.config['DM_API_AUTH_TOKENS']
        app.config['DM_API_AUTH_TOKENS'] = valid_token

    def do_not_provide_access_token(self):
        self.app.wsgi_app = self.app.wsgi_app.app

    def setup_dummy_user(self, id=123, role='buyer'):
        with self.app.app_context():
            if User.query.get(id):
                return id
            user = User(
                id=id,
                email_address="test+{}@digital.gov.au".format(id),
                name="my name",
                password="fake password",
                active=True,
                role=role,
                password_changed_at=datetime.now()
            )
            db.session.add(user)
            db.session.commit()

            return user.id

    def setup_dummy_briefs(self, n, title=None, status='draft', user_id=1, data=None,
                           brief_start=1, lot="digital-specialists", published_at=None):
        user_id = self.setup_dummy_user(id=user_id)

        with self.app.app_context():
            framework = Framework.query.filter(Framework.slug == "digital-outcomes-and-specialists").first()
            lot = Lot.query.filter(Lot.slug == lot).first()
            data = data or COMPLETE_DIGITAL_SPECIALISTS_BRIEF.copy()
            data["title"] = title
            for i in range(brief_start, brief_start + n):
                self.setup_dummy_brief(
                    id=i,
                    user_id=user_id,
                    data=data,
                    framework_slug="digital-outcomes-and-specialists",
                    lot_slug=lot.slug,
                    status=status,
                    published_at=published_at,
                )
            db.session.commit()

    def setup_dummy_brief(
        self, id=None, user_id=1, status=None, data=None, published_at=None, withdrawn_at=None,
        framework_slug="digital-outcomes-and-specialists", lot_slug="digital-specialists"
    ):
        if published_at is not None and status is not None:
            raise ValueError("Cannot provide both status and published_at")
        if withdrawn_at is not None and publish_at is None:
            raise ValueError("If setting withdrawn_at then published_at must also be set")
        if not published_at:
            if status == 'closed':
                published_at = datetime.utcnow() - timedelta(days=1000)
            elif status == 'withdrawn':
                published_at = datetime.utcnow() - timedelta(days=1000)
                withdrawn_at = datetime.utcnow()
            else:
                published_at = None if status == 'draft' else datetime.utcnow()
        framework = Framework.query.filter(Framework.slug == framework_slug).first()
        lot = Lot.query.filter(Lot.slug == lot_slug).first()

        db.session.add(Brief(
            id=id,
            data=data,
            framework=framework,
            lot=lot,
            users=[User.query.get(user_id)],
            published_at=published_at,
            withdrawn_at=withdrawn_at,
        ))

    def setup_dummy_suppliers(self, n):
        with self.app.app_context():
            for i in range(n):
                db.session.add(
                    Supplier(
                        code=(i),
                        name=u"Supplier {}".format(i),
                        description="",
                        summary="",
                        address=Address(address_line="{} Dummy Street".format(i),
                                        suburb="Dummy",
                                        state="ZZZ",
                                        postal_code="0000",
                                        country='Australia'),
                        contacts=[],
                        references=[],
                        prices=[],
                    )
                )
            db.session.commit()

    def setup_additional_dummy_suppliers(self, n, initial):
        with self.app.app_context():
            for i in range(1000, n+1000):
                db.session.add(
                    Supplier(
                        code=str(i),
                        name=u"{} suppliers Ltd {}".format(initial, i),
                        description="",
                        summary="",
                        address=Address(address_line="{} Additional Street".format(i),
                                        suburb="Additional",
                                        state="ZZZ",
                                        postal_code="0000",
                                        country='Australia'),
                        contacts=[],
                        references=[],
                        prices=[],
                    )
                )
            db.session.commit()

    def setup_dummy_service(self, service_id, supplier_code=1, data=None,
                            status='published', framework_id=1, lot_id=1):
        now = datetime.utcnow()
        db.session.add(Service(service_id=service_id,
                               supplier_code=supplier_code,
                               status=status,
                               data=data or {
                                   'serviceName': 'Service {}'.
                                                  format(service_id)
                               },
                               framework_id=framework_id,
                               lot_id=lot_id,
                               created_at=now,
                               updated_at=now))

    def setup_dummy_services(self, n, supplier_code=None, framework_id=1,
                             start_id=0, lot_id=1):
        with self.app.app_context():
            for i in range(start_id, start_id + n):
                self.setup_dummy_service(
                    service_id=str(2000000000 + start_id + i),
                    supplier_code=supplier_code or (i % TEST_SUPPLIERS_COUNT),
                    framework_id=framework_id,
                    lot_id=lot_id
                )

            db.session.commit()

    def setup_dummy_services_including_unpublished(self, n):
        self.setup_dummy_suppliers(TEST_SUPPLIERS_COUNT)
        self.setup_dummy_services(n)
        with self.app.app_context():
            # Add extra 'enabled' and 'disabled' services
            self.setup_dummy_service(
                service_id=str(n + 2000000001),
                supplier_code=n % TEST_SUPPLIERS_COUNT,
                status='disabled')
            self.setup_dummy_service(
                service_id=str(n + 2000000002),
                supplier_code=n % TEST_SUPPLIERS_COUNT,
                status='enabled')
            # Add an extra supplier that will have no services
            db.session.add(
                Supplier(code=TEST_SUPPLIERS_COUNT, name=u"Supplier {}"
                         .format(TEST_SUPPLIERS_COUNT),
                         address=Address(address_line="{} Empty Street".format(TEST_SUPPLIERS_COUNT),
                                         suburb="Empty",
                                         state="ZZZ",
                                         postal_code="0000",
                                         country='Australia'),
                         )
            )
            db.session.commit()

    def teardown(self):
        self.teardown_authorization()
        self.teardown_database()

    def teardown_authorization(self):
        if self._auth_tokens is None:
            del self.app.config['DM_API_AUTH_TOKENS']
        else:
            self.app.config['DM_API_AUTH_TOKENS'] = self._auth_tokens

    def teardown_database(self):
        with self.app.app_context():
            db.session.remove()
            for table in reversed(db.metadata.sorted_tables):
                if table.name not in ["lot", "framework", "framework_lot", "service_category", "service_role"]:
                    db.engine.execute(table.delete())
            FrameworkLot.query.filter(FrameworkLot.framework_id >= 100).delete()
            Framework.query.filter(Framework.id >= 100).delete()
            db.session.commit()
            db.get_engine(self.app).dispose()

    def load_example_listing(self, name):
        file_path = os.path.join("example_listings", "{}.json".format(name))
        with open(file_path) as f:
            return json.load(f)

    def string_to_time_to_string(self, value, from_format, to_format):
        return datetime.strptime(
            value, from_format).strftime(to_format)

    def string_to_time(self, value, from_format):
        return datetime.strptime(
            value, from_format)

    def set_framework_status(self, slug, status):
        Framework.query.filter_by(slug=slug).update({'status': status})
        db.session.commit()


class JSONTestMixin(object):
    """
    Tests to verify that endpoints that accept JSON.
    """
    endpoint = None
    method = None
    client = None

    def open(self, **kwargs):
        return self.client.open(
            self.endpoint.format(self=self),
            method=self.method,
            **kwargs
        )

    def test_non_json_causes_failure(self):
        response = self.open(
            data='this is not JSON',
            content_type='application/json')

        assert_equal(response.status_code, 400)
        assert_in(b'Invalid JSON',
                  response.get_data())

    def test_invalid_content_type_causes_failure(self):
        response = self.open(
            data='{"services": {"foo": "bar"}}')

        assert_equal(response.status_code, 400)
        assert_in(b'Unexpected Content-Type', response.get_data())


class JSONUpdateTestMixin(JSONTestMixin):
    @pytest.mark.skipif(True, reason="failing for AU")
    def test_missing_updated_by_should_fail_with_400(self):
        response = self.open(
            data='{}',
            content_type='application/json')

        assert_equal(response.status_code, 400)
        assert_in("'updated_by' is a required property", response.get_data(as_text=True))


def isRecentTimestamp(timestamp):
    now = getUtcTimestamp()
    return now - timestamp < timedelta(seconds=10)
