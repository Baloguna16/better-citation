from flask import Flask, Blueprint, flash, redirect, render_template, request, session, url_for, send_file

from support.forms import FlaskForm, BasicForm, AdvancedForm, ManualForm
from scraper.nytimes import create_citation_nyt
from scraper.journalism import create_citation_journalism
from scraper.sd import create_citation_sd
from format.manual import create_citation_manual

bp = Blueprint('/routes', __name__)

@bp.route('/')
def index():
    pass #space holder
    return redirect('/citation')

@bp.route('/citation', methods=['POST', 'GET'])
def citation():
    form = BasicForm()
    if form.validate_on_submit():
        link = form.link.data
        session['link'] = link
        return redirect('/engine')
    for field_name, error_messages in form.errors.items():
            for err in error_messages:
                flash('Check {}. {}'.format(field_name, err))
    return render_template('engine/citation.html', form=form)

@bp.route('/manual', methods=['POST', 'GET'])
def manual():
    form = ManualForm()
    if form.validate_on_submit():
        citation = create_citation_manual(form)
        session['citations'] = [citation]
        return redirect('/complete')
    for field_name, error_messages in form.errors.items():
            for err in error_messages:
                flash('Check {}. {}'.format(field_name, err))
    return render_template('engine/manual.html', form=form)

@bp.route('/engine')
def engine():
    link = session['link']
    if "nytimes.com" in link:
        citation = create_citation_nyt(link, 'mla') #NYT only
    elif "sciencedirect.com" in link:
        citation = create_citation_sd(link, 'mla') #sciencedirect
    else:
        citation = create_citation_journalism(link, 'mla') #other
    session['citations'] = [citation]
    return redirect('/complete')

@bp.route('/complete')
def complete():
    display_citations = session['citations']
    flash('Your citation is complete. Copy below.')
    # today = datetime.today().strftime('%d-%m-%Y-%H%M%S%f')
    # filename = "raw_" + today + ".txt"
    # with open('static/temporaries/' + filename, 'a+', newline='') as file:
    #     file.write(citation)
    return render_template('engine/complete.html', display_citations=display_citations)

@bp.route('/download/<filename>')
def download(filename):
    today = datetime.now().strftime("-%Y-%m-%d")
    return send_file('static/temporaries/' + filename,
                     mimetype='text/csv',
                     attachment_filename=filename,
                     as_attachment=True)

@bp.route('/about')
def about():
    pass
    return render_template('manage/about.html')
