from project import db #project refers to __init__.py file of project directory
from flask import session
from flask import current_app

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    answer_text = db.Column(db.Text)
    asked_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expert_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    asked_by_user = db.relationship("Users", foreign_keys=[asked_by_id])
    expert_user = db.relationship("Users", foreign_keys=[expert_id])

    @classmethod
    def get_all_answered_questions_details(cls):
        current_app.logger.info("Inside get_all_answered_question method of questions model")
        questions = []
        results = cls.query.filter(cls.answer_text != None).all()
        for result in results:
            temp = {}
            temp['id'] = result.id
            temp['question'] = result.question_text
            temp['asked_by'] = result.asked_by_user.name
            temp['expert'] = result.expert_user.name
            questions.append(temp)
        return questions

    @classmethod
    def get_question_details(cls, question_id):
        question = cls.query.filter_by(id=question_id).first()
        return question

    @classmethod
    def view_question_details(cls, question_id):
        question = cls.query.filter_by(id=question_id).first()
        question_details = {}
        question_details['question'] = question.question_text
        question_details['answer'] = question.answer_text
        question_details['asked_by'] = question.asked_by_user.name
        question_details['expert'] = question.expert_user.name
        return question_details

    @classmethod
    def get_unanswered_questions(cls, expert_id):
        questions = []
        questions_list = cls.query.filter(cls.answer_text == None, cls.expert_id == expert_id).all()
        for question in questions_list:
            temp = {}
            temp['id'] = question.id
            temp['question_text'] = question.question_text
            temp['name'] = question.asked_by_user.name
            questions.append(temp)
        return questions

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()