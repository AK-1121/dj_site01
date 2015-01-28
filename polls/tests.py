import datetime, os, unittest

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from polls.models import Question, Choice

BASE_DIR=os.path.dirname(os.path.dirname(__file__))

# Create your tests here.
class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions
        whose pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question=Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose 
        pub_date is older than 1 day
        """
        time = timezone.now()-datetime.timedelta(days=30)
        old_question=Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for question whose
        pub_date is within the last day
        """
        time=timezone.now()-datetime.timedelta(hours=1)
        recent_question=Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    Creates a question with the given 'question_text' published
    the given number of 'days' offset to now (negative for question 
    published in the past, positive for questions that have yet to be 
    published).
    """
    time = timezone.now()+datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,
                                   pub_date=time)

class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be displayed on the
        index page
        """

        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed
        on the index page.
        """
        create_question(question_text="Future question.", days=30)
        response=self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.",count=1,
                            status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past 
        questions should be displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_indext_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30.2)
        create_question(question_text="Past question 2.", days=-0.6)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
            #['<Question: Past question 1.>', '<Question: Past question 2.>'],
            #By deafault, the comparison is ordering dependent.
            #ordered=False
        )

class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        should return a 404 not found.
        """
        future_question=create_question(question_text='Future question.', days=5)
        response=self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        The detail view of a question with a pub_date in the past 
        should display the question's text.
        """
        past_question=create_question(question_text='Past Question.', days=-5)
        response=self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text, status_code=200)

class QuestionResultsTests(TestCase):
    def test_result_view_with_a_future_question(self):
        """
        The result view of a question with a pub_date in the future
        should return a 404 error (page not found).
        """
        future_question=create_question(question_text='Future question.', days=5)
        response=self.client.get(reverse('polls:results', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)
        #self.assertEqual(response.__dict__, 404)

    def test_result_view_with_a_past_question_with_answers(self):
        """
        The result view of a question with a pub_date in the past
        should display the question's text.
        """
        past_question=create_question(question_text='Past Question.', days=-3.2)

        time = timezone.now()
        choice1 = Choice.objects.create(choice_text="Choice_text1", 
            question_id=past_question.id, id=101, votes=7)
        choice2 = Choice.objects.create(choice_text="Choice_text2", 
            question_id=past_question.id, id=102, votes=5)
        choice3 = Choice.objects.create(choice_text="Choice_text3", 
            question_id=past_question.id+1, id=103, votes=11)
        choice4 = Choice.objects.create(choice_text="Choice_text4", 
            question_id=past_question.id, id=104, votes=0)


        f=open(os.path.join(BASE_DIR,'log_test'),'w')
        response=self.client.get(reverse('polls:results', args=(past_question.id,)))
        f.write("resp_container:\ntype:"+ str(type(response._container))+" xxxx "+
                str(response._container)+"\n\n\n"+str(response._container[0])+"\n\n")
        f.write("RESP:"+str(response)+"\n\nRes_DICT:\n"+str(response.__dict__)+
                "\n=============\nRESP_dir:\n"+str(dir(response)))
        self.assertContains(response, past_question.question_text, status_code=200)
        #self.assertContains(str(response._container[0]), "Choice_text3")
        self.assertTrue("Choice_text4" in str(response._container[0]) and "Choice_text3" not in 
                        str(response._container[0]))
        f.close()

    #@unittest.skip("I have to find out in the future, how to check question without choices.")
    def test_result_view_with_a_past_question_without_answers(self):
        """
        The result view of a question with a pub_date in the past without answers
        should display the question's text with warning.
        """
        #f=open(os.path.join(BASE_DIR,'log_test_without_questions'),'w+')
        past_question=create_question(question_text='Past Question.', days=0)
        response = self.client.get(reverse('polls:results', args=(past_question.id,)))
        #f.write("resp_container:\ntype:"+ str(type(response._container))+" xxxx "+
        #        str(response._container)+"\n\n\n"+str(response._container[0])+"\n\n")
        self.assertContains(response, past_question.question_text, status_code=200)
        #("I have to find out in the future, how to check question without choices."
        #self.assertTrue("There is no answers." in str(response._container[0]))




   




