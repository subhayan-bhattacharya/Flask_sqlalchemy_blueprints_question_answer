from werkzeug.security import generate_password_hash, check_password_hash
from flask import session,render_template,redirect,url_for,Blueprint,request,flash
from project.questions.forms import AskForm,AnswerForm
from project.models.questions_model import Questions
from project.models.users_model import Users
from flask import current_app


questions_blueprint = Blueprint(
    'questions',
    __name__,
    template_folder='templates/questions'
)

@questions_blueprint.route('/answer/<question_id>',methods=["GET","POST"])
def answer(question_id):
    current_app.logger.debug('Inside answer route for question id : %s',str(question_id))
    user_details = Users.get_current_user()
    answerform = AnswerForm()

    if answerform.validate_on_submit():
        answer = answerform.answer.data
        question = Questions.get_question_details(question_id=question_id)
        question.answer_text = answer
        question.save_to_db()
        current_app.logger.debug('Redirecting to unanswered route of questions blueprint')
        return redirect(url_for('questions.unanswered'))

    if user_details:
        if user_details.expert:
            question = Questions.get_question_details(question_id=question_id)
            return render_template('answer.html',user=user_details,question=question,form=answerform)
        else:
            current_app.logger.debug('Redirecting to index route of questions blueprint')
            return redirect(url_for('questions.index'))
    else:
        current_app.logger.debug('Redirecting to login route of users blueprint')
        return redirect(url_for('users.login'))

@questions_blueprint.route('/ask',methods=["GET","POST"])
def ask():
    current_app.logger.debug('Inside ask route of questions blueprint')
    user_details = Users.get_current_user()

    askform = AskForm()

    if request.method == "POST":
        if askform.validate_on_submit():
            question = askform.question.data
            expert_id = askform.expert.data
            ask_by_id = user_details.id
            new_question = Questions(question_text=question,asked_by_id=ask_by_id,expert_id=expert_id)
            new_question.save_to_db()
            current_app.logger.debug('Redirecting to index route of questions blueprint')
            return redirect(url_for('questions.index'))

    if user_details:
        return render_template('ask.html',user=user_details,form=askform)
    else:
        current_app.logger.debug('Redirecting to login route of users blueprint')
        return redirect(url_for('users.login'))

@questions_blueprint.route('/')
def index():
    current_app.logger.debug('Inside index route of questions blueprint')
    user_details = Users.get_current_user()
    results = Questions.get_all_answered_questions_details()
    return render_template('home.html',user=user_details,results=results)


@questions_blueprint.route('/question/<question_id>')
def question(question_id):
    current_app.logger.debug('Inside question route of questions blueprint for question id %s',str(question_id))
    user_details = Users.get_current_user()
    details = Questions.view_question_details(question_id)
    return render_template('question.html',user=user_details,details=details)


@questions_blueprint.route('/unanswered')
def unanswered():
    current_app.logger.debug('Inside unanswered route of questions blueprint')
    user_details = Users.get_current_user()
    if user_details:
        if user_details.expert:
            unanswered_questions = Questions.get_unanswered_questions(user_details.id)
            return render_template('unanswered.html',user=user_details,questions=unanswered_questions)
        else:
            current_app.logger.debug('Redirecting to index route of questions blueprint')
            return redirect(url_for('questions.index'))
    else:
        current_app.logger.debug('Redirecting to login route of users blueprint')
        return redirect(url_for('users.login'))

