from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from . import main 
from flask_login import login_required, current_user
from .forms import UpdateProfile, GeneralForm, GeneralReviewForm, SaleForm, SaleReviewForm, SeductionForm, SeductionReviewForm, MusicForm, MusicReviewForm, ProjectForm, ProjectReviewForm, InterviewForm, InterviewReviewForm, AdvertisementForm, AdvertisementReviewForm
from .. import db
from sqlalchemy import func
from ..models import User, Interview, Advertisement, Project, Music, Sale, Seduction, General, ReviewAdvertisement, ReviewGeneral, ReviewInterview, ReviewMusic, ReviewProject, ReviewSale, ReviewSeduction, Upvote, Downvote

@main.route('/')
def index():
    """
    View root page function that returns the index page and its data
    """
    title = 'Home - Welcome to The Pitch website'

    return render_template('index.html', title=title)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/',methods = ['GET', 'POST'])

def index():

    '''
    View root page function that returns the index page and its data
    '''
    general = Pitch.query.filter_by(category="general").order_by(Pitch.posted.desc()).all()
    project = Pitch.query.filter_by(category="project").order_by(Pitch.posted.desc()).all()
    advertisement = Pitch.query.filter_by(category="advertisement").order_by(Pitch.posted.desc()).all()
    sale = Pitch.query.filter_by(category="sale").order_by(Pitch.posted.desc()).all()

    pitch = Pitch.query.filter_by().first()
    likes = Like.get_all_likes(pitch_id=Pitch.id)
    dislikes = Dislike.get_all_dislikes(pitch_id=Pitch.id)


    title = 'Home | One Min Pitch'
    return render_template('index.html', title = title, pitch = pitch, general = general, project = project, advertisement = advertisement, sale = sale, likes=likes, dislikes=dislikes)



@main.route('/user/<uname>')
def profile(uname):
    '''
    View profile page function that returns the profile page and its data
    '''
    user = User.query.filter_by(username = uname).first()
    title = f"{uname.capitalize()}'s Profile"

    get_pitches = Pitch.query.filter_by(author = User.id).all()
    get_comments = Comment.query.filter_by(user_id = User.id).all()
    get_likes = Like.query.filter_by(user_id = User.id).all()
    get_dislikes = Dislike.query.filter_by(user_id = User.id).all()

    if user is None:
        abort (404) 

    return render_template("profile/profile.html", user = user, title=title, pitches_no = get_pitches, comments_no = get_comments, likes_no = get_likes, dislikes_no = get_dislikes)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    '''
    View update profile page function that returns the update profile page and its data
    '''
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods=['POST'])
@login_required
def update_pic(uname):
    '''
    View update pic profile function that returns the uppdate profile pic page
    '''
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))



@main.route('/home', methods = ['GET', 'POST'])
@login_required
def index2():
    '''
    View index2 function that returns the home page
    '''
    advertisement = Pitch.query.filter_by(category="advertisement").order_by(Pitch.date.desc()).all()
    project = Pitch.query.filter_by(category="project").order_by(Pitch.date.desc()).all()
    general = Pitch.query.filter_by(category="general").order_by(Pitch.date.desc()).all()
    sale = Pitch.query.filter_by(category="sale").order_by(Pitch.date.desc()).all()
    pitch = Pitch.get_all_pitches()

    title = 'Home | One Min Pitch'
    return render_template('home.html', title = title, pitch = pitch, advertisement = advertisement, project = project, general = general, sale = sale)


@main.route('/pitch/new',methods = ['GET','POST'])
@login_required
def pitch():
    '''
    View pitch function that returns the pitch page and data
    '''
    pitch_form = PitchForm()
    likes = Like.query.filter_by(pitch_id=Pitch.id)

    if pitch_form.validate_on_submit():
        body = pitch_form.body.data
        category = pitch_form.category.data
        title = pitch_form.title.data

        new_pitch = Pitch(title=title, body=body, category = category, user = current_user)
        new_pitch.save_pitch()

        return redirect(url_for('main.index'))


    title = 'New Pitch | One Minute Pitch'
    return render_template('pitch.html', title = title, pitch_form = pitch_form, likes = likes)


@main.route('/pitch/<int:pitch_id>/comment',methods = ['GET', 'POST'])
@login_required
def comment(pitch_id):
    '''
    View comments page function that returns the comment page and its data
    '''

    comment_form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    if pitch is None:
        abort(404)

    if comment_form.validate_on_submit():
        comment_body = comment_form.comment_body.data

        new_comment = Comment(comment=comment_body, pitch_id = pitch_id, user = current_user)
        new_comment.save_comment()

        return redirect(url_for('.comment', pitch_id=pitch_id))

    comments = Comment.query.filter_by(pitch_id=pitch_id).all()
    title = 'New Comment | One Min Pitch'

    return render_template('comment.html', title = title, pitch=pitch ,comment_form = comment_form, comment = comments )





@main.route('/pitch/<int:pitch_id>/like',methods = ['GET','POST'])
@login_required
def like(pitch_id):
    '''
    View like function that returns likes
    '''
    pitch = Pitch.query.get(pitch_id)
    user = current_user

    likes = Like.query.filter_by(pitch_id=pitch_id)


    if Like.query.filter(Like.user_id==user.id,Like.pitch_id==pitch_id).first():
        return  redirect(url_for('.index'))

    new_like = Like(pitch_id=pitch_id, user = current_user)
    new_like.save_likes()
    return redirect(url_for('.index'))



@main.route('/pitch/<int:pitch_id>/dislike',methods = ['GET','POST'])
@login_required
def dislike(pitch_id):
    '''
    View dislike function that returns dislikes
    '''
    pitch = Pitch.query.get(pitch_id)
    user = current_user

    pitch_dislikes = Dislike.query.filter_by(pitch_id=pitch_id)

    if Dislike.query.filter(Dislike.user_id==user.id,Dislike.pitch_id==pitch_id).first():
        return redirect(url_for('.index'))

    new_dislike = Dislike(pitch_id=pitch_id, user = current_user)
    new_dislike.save_dislikes()
    return redirect(url_for('.index'))



@main.route('/user/category/advertisement', methods=['GET', 'POST'])
@login_required
def advertisement():
    form = AdvertisementForm()
    title = 'Post a pitch'
    if form.validate_on_submit():
        post = form.post.data
        body = form.body.data
        new_advertisement = Advertisement(post=post, user=current_user, body=body)
        new_advertisement.save_advertisement()
        return redirect(url_for('.advertisements'))
    return render_template("advertisement.html", advertisement_form=form, title=title)


@main.route('/user/category/project', methods=['GET', 'POST'])
@login_required
def project():
    form = ProjectForm()
    title = 'Post a pitch'
    if form.validate_on_submit():
        post = form.post.data
        body = form.body.data
        new_project = Project(post=post, user=current_user, body=body)
        new_project.save_project()
        return redirect(url_for('.projects'))
    return render_template("project.html", project_form=form, title=title)


@main.route('/user/category/music', methods=['GET', 'POST'])
@login_required
def music():
    form = MusicForm()
    title = 'Post a pitch'
    if form.validate_on_submit():
        post = form.post.data
        body = form.body.data
        new_music = Music(post=post, user=current_user, body=body)
        new_music.save_music()
        return redirect(url_for('.musics'))
    return render_template("music.html", music_form=form, title=title)


@main.route('/user/category/interview', methods=['GET', 'POST'])
@login_required
def interview():
    form = InterviewForm()
    title = 'Post a pitch'
    if form.validate_on_submit():
        post = form.post.data
        body = form.body.data
        new_interview = Interview(post=post, user=current_user, body=body)
        new_interview.save_interview()
        return redirect(url_for('.interviews'))
    return render_template("interview.html", interview_form=form, title=title)


@main.route('/user/category/seduction', methods=['GET', 'POST'])
@login_required
def seduction():
    form = SeductionForm()
    title = 'Post a pitch'
    if form.validate_on_submit():
        post = form.post.data
        body = form.body.data
        new_seduction = Seduction(post=post, user=current_user, body=body)
        new_seduction.save_seduction()
        return redirect(url_for('.seductions'))
    return render_template("seduction.html", seduction_form=form, title=title)


@main.route('/user/category/sale', methods=['GET', 'POST'])
@login_required
def sale():
    form = SaleForm()
    title = 'Post a pitch'
    if form.validate_on_submit():
        post = form.post.data
        body = form.body.data
        new_sale = Sale(post=post, user=current_user, body=body)
        new_sale.save_sale()
        return redirect(url_for('.sales'))
    return render_template("sale.html", sale_form=form, title = title)


@main.route('/user/category/general', methods=['GET', 'POST'])
@login_required
def general():
    form = GeneralForm()
    title = 'Post a pitch'
    if form.validate_on_submit():
        post = form.post.data
        body = form.body.data
        new_general = General(post=post, user=current_user, body=body)
        new_general.save_general()
        return redirect(url_for('.generals'))
    return render_template("general.html", general_form=form, title=title)


@main.route('/user/category/advertisements')
@login_required
def advertisements():
    title = 'Advertisement'
    posts = Advertisement.query.all()
    return render_template("advert.html", posts=posts, title=title)


@main.route('/user/advertisement/<int:id>', methods=['POST', 'GET'])
@login_required
def displayadvertisement(id):
    advertisement = Advertisement.query.get(id)
    form = AdvertisementReviewForm()
    if form.validate_on_submit():
        review = form.review.data
        new_advertisementreview = ReviewAdvertisement(
            review=review, advertisement_id=id, user=current_user)
        new_advertisementreview.save_reviewadvertisement()

    review = ReviewAdvertisement.query.filter_by(advertisement_id=id).all()
    return render_template('advertpitch.html', advertisement=advertisement, review_form=form, review=review)

@main.route('/user/category/projects')
@login_required
def projects():
    title = 'Project'
    posts = Project.query.all()
    return render_template("proj.html", posts=posts, title=title)


@main.route('/user/project/<int:id>', methods=['POST', 'GET'])
@login_required
def displayproject(id):
    project = Project.query.get(id)
    form = ProjectReviewForm()
    if form.validate_on_submit():
        review = form.review.data
        new_projectreview = ReviewProject(
            review=review, project_id=id, user=current_user)
        new_projectreview.save_reviewproject()

    review = ReviewProject.query.filter_by(project_id=id).all()
    return render_template('projectpitch.html', project=project, review_form=form, review=review)

@main.route('/user/category/musics')
@login_required
def musics():
    title = 'Music'
    posts = Music.query.all()
    return render_template("misc.html", posts=posts, title=title)


@main.route('/user/music/<int:id>', methods=['POST', 'GET'])
@login_required
def displaymusic(id):
    music = Music.query.get(id)
    form = MusicReviewForm()
    if form.validate_on_submit():
        review = form.review.data
        new_musicreview = ReviewMusic(
            review=review, music_id=id, user=current_user)
        new_musicreview.save_reviewmusic()

    review = ReviewMusic.query.filter_by(music_id=id).all()
    return render_template('musicpitch.html', music=music, review_form=form, review=review)


@main.route('/user/category/seductions')
@login_required
def seductions():
    title = 'Seduction'
    posts = Seduction.query.all()
    return render_template("seduct.html", posts=posts, title=title)


@main.route('/user/seduction/<int:id>', methods=['POST', 'GET'])
@login_required
def displayseduction(id):
    seduction = Seduction.query.get(id)
    form = SeductionReviewForm()
    if form.validate_on_submit():
        review = form.review.data
        new_seductionreview = ReviewSeduction(
            review=review, seduction_id=id, user=current_user)
        new_seductionreview.save_reviewseduction()

    review = ReviewSeduction.query.filter_by(seduction_id=id).all()
    return render_template('seductpitch.html', seduction=seduction, review_form=form, review=review)


@main.route('/user/category/sales')
@login_required
def sales():
    title = 'Sale'
    posts = Sale.query.all()
    return render_template("sal.html", posts=posts, title=title)


@main.route('/user/sale/<int:id>', methods=['GET', 'POST'])
@login_required
def displaysale(id):
    sale = Sale.query.get(id)
    form = SaleReviewForm()
    if form.validate_on_submit():
        review = form.review.data
        new_salereview = ReviewSale(
            review=review, sale_id=id, user=current_user)
        new_salereview.save_reviewsale()

    review = ReviewSale.query.filter_by(sale_id=id).all()
    return render_template('salepitch.html', sale=sale, review_form=form, review=review)


@main.route('/user/categor/generals')
@login_required
def generals():
    title = 'General'
    posts = General.query.all()
    return render_template("gen.html", posts=posts, title=title)

@main.route('/user/general/<int:id>', methods=['GET', 'POST'])
@login_required
def displaygeneral(id):
    general = General.query.get(id)
    form = GeneralReviewForm()
    if form.validate_on_submit():
        review = form.review.data
        new_generalreview = ReviewGeneral(
            review=review, general_id=id, user=current_user)
        new_generalreview.save_reviewgeneral()

    review = ReviewGeneral.query.filter_by(general_id=id).all()
    return render_template('genpitch.html', general=general, review_form=form, review=review)


@main.route('/user/rating')
@login_required
def ratings():
    upvote = Upvote(user=current_user)
    upvote.save_upvote()
    votes = db.session.query(func.sum(Upvote.upvote)).scalar()
    votes = str(votes)
    return votes


@main.route('/user/rating')
@login_required
def rating():
    downvote = Downvote(user=current_user)
    downvote.save_downvote()
    votes = db.session.query(func.sum(Downvote.downvote)).scalar()
    votes = str(votes)
    return votes


@main.route('/user/category/interviews')
@login_required
def interviews():
    title = 'Interview'
    posts = Interview.query.all()
    return render_template("inter.html", posts=posts, title=title)


@main.route('/user/interview/<int:id>', methods=['GET', 'POST'])
@login_required
def displayinterview(id):
    interview = Interview.query.get(id)
    form = InterviewReviewForm()
    if form.validate_on_submit():
        review = form.review.data
        new_interviewreview = ReviewInterview(
            review=review, interview_id=id, user=current_user)
        new_interviewreview.save_reviewinterview()

    review = ReviewInterview.query.filter_by(interview_id=id).all()
    return render_template('interviewpitch.html', interview=interview, review_form=form, review=review)