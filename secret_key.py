import secrets

def generate_secret_key():
    return secrets.token_hex(16)  # Generates a 32-character hexadecimal string

# Example usage
if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("Generated Secret Key:", secret_key)


# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <meta http-equiv="X-UA-Compatible" content="ie=edge">
#     <title>{% block title %}Default Page{% endblock %}</title>
#     <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
#     <style>
#         .navbar-nav .nav-item .nav-link {
#             color: white !important;
#         }
#         .flashes {
#             list-style-type: none;
#             padding: 0;
#             margin: 10px 0;
#         }
#         .flash {
#             padding: 10px;
#             margin: 5px 0;
#             border-radius: 4px;
#         }
#         .flash.success { background-color: #d4edda; color: #155724; }
#         .flash.error { background-color: #f8d7da; color: #721c24; }
#     </style>
# </head>

# <body>
#     <header>
#         <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
#             <a class="navbar-brand" href="#">My Finance Tracker</a>
#             <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
#                 <span class="navbar-toggler-icon"></span>
#             </button>
#             <div class="collapse navbar-collapse" id="navbarNav">
#                 <ul class="navbar-nav ml-auto">
#                     <li class="nav-item">
#                         <a class="nav-link" href="{{ url_for('finance.index') }}">Finance Page</a>
#                     </li>
#                     <li class="nav-item">
#                         <a class="nav-link" href="{{ url_for('marketplace.index') }}">Market Page</a>
#                     </li>
#                     <li class="nav-item">
#                         <a class="nav-link" href="{{ url_for('core.logout') }}">Logout</a>
#                     </li>
#                 </ul>
#             </div>
#         </nav>
#     </header>

#     <main class="container my-5">
#         {% with messages = get_flashed_messages(with_categories=True) %}
#         {% if messages %}
#             <ul class="flashes">
#                 {% for category, message in messages %}
#                     <li class="flash {{ category }}">{{ message }}</li>
#                 {% endfor %}
#             </ul>
#         {% endif %}
#         {% endwith %}

#         {% block content %}{% endblock %}
#     </main>

#     <footer class="bg-dark text-white text-center py-3 mt-auto">
#         <p>&copy; 2024 My Website. All Rights Reserved.</p>
#     </footer>

#     <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
#     <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
# </body>
# </html>
