from flask_app import app

from flask_app.models.skeptic import Skeptic

from flask import render_template, request, redirect, flash, session


from flask_app.models.user import User  # Import the User model



@app.route('/add_skeptic/<int:sighting_id>', methods=['POST'])
def add_skeptic(sighting_id):
    user_id = session.get('user_id')

    if not user_id:
        flash("Please log in to mark yourself as skeptical.", 'skeptic_error')
        return redirect('/')

    # Check if the user is already skeptical of this sighting
    if Skeptic.is_user_skeptical(user_id, sighting_id):
        flash("You are already skeptical of this sighting.", 'skeptic_error')
        return redirect(f"/view/{sighting_id}")

    # Add the user to the list of skeptics for the sighting
    Skeptic.create_skeptic({'user_id': user_id, 'sighting_id': sighting_id})
    flash("You are now marked as skeptical of this sighting.", 'skeptic_success')
    return redirect(f"/view/{sighting_id}")

@app.route('/remove_skeptic/<int:sighting_id>', methods=['POST'])
def remove_skeptic(sighting_id):
    if 'user_id' not in session:
        flash("Please log in to remove your skepticism.", 'remove_skeptic_error')
        return redirect('/')

    user_id = session['user_id']

    # Remove the user from the skeptics list
    Skeptic.remove_skeptic(user_id, sighting_id)
    
    return redirect(f'/view/{sighting_id}')