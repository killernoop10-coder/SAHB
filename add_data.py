from app import app, db, Manual

with app.app_context():

    data = [

        Manual(
            question="default ip",
            answer="The default IP is 192.168.1.64"
        ),

        Manual(
            question="reset camera",
            answer="Hold the reset button for 15 seconds."
        ),

        Manual(
            question="admin password",
            answer="Default username: admin"
        )

    ]

    db.session.add_all(data)

    db.session.commit()

    print("Data added successfully.")