import json
from individual.tests.test_helpers import (
    create_group,
    IndividualGQLTestCase,
)


class GroupGQLMutationTest(IndividualGQLTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_create_group_general_permission(self):
        query_str = f'''
            mutation {{
              createGroup(
                input: {{
                  code: "GF"
                  individualsData: []
                }}
              ) {{
                clientMutationId
                internalId
              }}
            }}
        '''

        # Anonymous User has no permission
        response = self.query(query_str)

        content = json.loads(response.content)
        id = content['data']['createGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # IMIS admin can do everything
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.admin_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['createGroup']['internalId']
        self.assert_mutation_success(id)

        # Health Enrollment Officier (role=1) has no permission
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.med_enroll_officer_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['createGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

    def test_create_group_row_security(self):
        query_str = f'''
            mutation {{
              createGroup(
                input: {{
                  code: "GBVA"
                  individualsData: []
                  villageId: {self.village_a.id}
                }}
              ) {{
                clientMutationId
                internalId
              }}
            }}
        '''

        # SP officer B cannot create group for district A
        response = self.query(query_str)
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        id = content['data']['createGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # SP officer A can create group for district A
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_a_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['createGroup']['internalId']
        self.assert_mutation_success(id)

        # SP officer B can create group for district B
        response = self.query(
            query_str.replace(
                f'villageId: {self.village_a.id}',
                f'villageId: {self.village_b.id}'
            ), headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['createGroup']['internalId']
        self.assert_mutation_success(id)

        # SP officer B can create group without any district
        response = self.query(
            query_str.replace(f'villageId: {self.village_a.id}', ' '),
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['createGroup']['internalId']
        self.assert_mutation_success(id)

    def test_update_group_general_permission(self):
        group = create_group(self.admin_user.username)
        query_str = f'''
            mutation {{
              updateGroup(
                input: {{
                  id: "{group.id}"
                  code: "GFOO"
                }}
              ) {{
                clientMutationId
                internalId
              }}
            }}
        '''

        # Anonymous User has no permission
        response = self.query(query_str)

        content = json.loads(response.content)
        id = content['data']['updateGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # IMIS admin can do everything
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.admin_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['updateGroup']['internalId']
        self.assert_mutation_success(id)

        # Health Enrollment Officier (role=1) has no permission
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.med_enroll_officer_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['updateGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

    def test_update_group_row_security(self):
        group_a = create_group(
            self.admin_user.username,
            payload_override={'village': self.village_a},
        )
        query_str = f'''
            mutation {{
              updateGroup(
                input: {{
                  id: "{group_a.id}"
                  code: "GBAR"
                }}
              ) {{
                clientMutationId
                internalId
              }}
            }}
        '''

        # SP officer B cannot update group for district A
        response = self.query(query_str)
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        id = content['data']['updateGroup']['internalId']
        self.assert_mutation_error(id, 'mutation.authentication_required')

        # SP officer A can update group for district A
        response = self.query(
            query_str,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_a_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['updateGroup']['internalId']
        self.assert_mutation_success(id)

        # SP officer B can update group without any district
        group_no_loc = create_group(self.admin_user.username)
        response = self.query(
            query_str.replace(
                f'id: "{group_a.id}"',
                f'id: "{group_no_loc.id}"'
            ), headers={"HTTP_AUTHORIZATION": f"Bearer {self.dist_b_user_token}"}
        )
        content = json.loads(response.content)
        id = content['data']['updateGroup']['internalId']
        self.assert_mutation_success(id)
