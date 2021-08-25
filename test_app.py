import unittest

from app import app


class FlaskTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_all_teachers(self):
        tester = app.test_client(self)
        response = tester.get('/all/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_teachers_by_goal(self):
        tester = app.test_client(self)
        travel_response = tester.get('/goals/travel/', content_type='html/text')
        self.assertEqual(travel_response.status_code, 200)
        study_response = tester.get('/goals/study/', content_type='html/text')
        self.assertEqual(study_response.status_code, 200)
        work_response = tester.get('/goals/work/', content_type='html/text')
        self.assertEqual(work_response.status_code, 200)
        relocate_response = tester.get('/goals/relocate/', content_type='html/text')
        self.assertEqual(relocate_response.status_code, 200)
        coding_response = tester.get('/goals/coding/', content_type='html/text')
        self.assertEqual(coding_response.status_code, 200)

    def test_teacher_profile(self):
        tester = app.test_client(self)
        response = tester.get('/profiles/1/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_request_select(self):
        tester = app.test_client(self)
        response = tester.post('/request/', data=dict(goal='Для путешествий', time='1-2 часа в неделю',
                                                      name='Denis', phone='+70002313513'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytes("Запрос отправлен!", 'utf-8'), response.data)

    def test_booking_teacher(self):
        tester = app.test_client(self)
        response = tester.post(
            '/booking/1/mon/12/', data=dict(name='Denis', phone='+70002313513'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytes("Скоро мы вам перезвоним", 'utf-8'), response.data)


if __name__ == '__main__':
    unittest.main()
