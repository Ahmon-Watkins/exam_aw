from flask_app import app


from flask import render_template, request, redirect, flash, session


from flask_app.models.sighting import Sighting
from flask_app.models.user import  User
from flask_app.models.skeptic import Skeptic
#Create
@app.route('/new/sighting')
def new_sighting():

    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/')

    user = User.get_one(user_id)
    if user is None:
        flash("User not found")
        return redirect('/')
    return render_template('new_sighting.html', user=user )
@app.route('/create/sighting', methods=["POST"])
def create_sighting():
    if 'user_id' not in session:
        flash("Please log in to create_sighting", 'sighting_post_error')
        return redirect('/')
    
    data = {
        "location": request.form["location"],
        "what_happened": request.form["what_happened"],
        "date_of_sighting": request.form["date_of_sighting"],
        "sasquatch_count": request.form["sasquatch_count"],
        "user_id": session["user_id"]
    }

    if not Sighting.validate_sighting(data):
        return redirect("/new/sighting")
    
    Sighting.create_sighting(data)
    print('working')
    print(data)
    
    return redirect(f"/dashboard/{session['user_id']}")
#read
@app.route('/view/<int:sighting_id>', methods=['GET'])
def view_sighting(sighting_id):
    sighting = Sighting.get_sighting_by_id_with_creator(sighting_id)
    if not sighting:
        flash("Sighting not found.", 'view_sighting_error')
        return redirect(f"/dashboard/{session['user_id']}")

    # Fetch the creator of the sighting
    creator = sighting.creator

    # Fetch the skeptics for the sighting
    skeptics = Skeptic.get_users_skeptical_of_sighting(sighting_id)

    return render_template('view_sighting.html', sighting=sighting, session_user=session, creator=creator, skeptics=skeptics)





#edit sighting

@app.route('/edit/<int:sighting_id>', methods=['GET', 'POST'])
def edit_sighting(sighting_id):
    if 'user_id' not in session:
        flash("Please log in to edit a sighting.", 'edit_sighting_error')
        return redirect('/')

    sighting = Sighting.get_sighting_by_id_with_creator(sighting_id)
    if sighting is None:
        flash("Sighting not found.", 'edit_sighting_error')
        return redirect('/dashboard')

    if sighting.user_id != session['user_id']:
        flash("You can only edit your own sightings.", 'edit_sighting_error')
        return redirect('/dashboard')

    if request.method == 'POST':
        data = {
            "id": sighting_id,
            "location": request.form["location"],
            "what_happened": request.form["what_happened"],
            "date_of_sighting": request.form["date_of_sighting"],
            "sasquatch_count": request.form["sasquatch_count"],
            "user_id": session["user_id"]
        }

        if not Sighting.validate_sighting(data):
            return redirect(f'/edit/{sighting_id}')

        Sighting.edit_sighting(data)
        flash("Sighting updated successfully.", 'edit_sighting_success')
        return redirect(f"/dashboard/{session['user_id']}")

    return render_template('edit_sighting.html', sighting=sighting)

# Delete
@app.route('/delete/<int:sighting_id>', methods=['POST'])
def delete_sighting(sighting_id):
    if 'user_id' not in session:
        flash("Please log in to delete a sighting.", 'delete_sighting_error')
        return redirect('/')

    sighting = Sighting.get_sighting_by_id(sighting_id)
    if not sighting:
        flash("Sighting not found.", 'delete_sighting_error')
        return redirect('/dashboard')

    if sighting.user_id != session['user_id']:
        flash("You can only delete your own sightings.", 'delete_sighting_error')
        return redirect('/dashboard')

    Sighting.delete_sighting(sighting_id)
    flash("Sighting deleted successfully.", 'delete_sighting_success')
    return redirect(f"/dashboard/{session['user_id']}")

    
