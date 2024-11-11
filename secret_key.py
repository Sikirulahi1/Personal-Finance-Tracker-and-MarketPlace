import secrets

def generate_secret_key():
    return secrets.token_hex(16)  # Generates a 32-character hexadecimal string

# Example usage
if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("Generated Secret Key:", secret_key)


# {% extends 'base.html' %}

# {% block title %} Homepage {% endblock %}

# {% block content %}
#     <div class="container mt-5">
#         {% if current_user.is_authenticated %}
#             <div class="text-center mb-4">
#                 <h1 class="display-4">Welcome, {{ current_user.username }}</h1>
#             </div>

#             <!-- Balance Overview Section -->
#             <div class="row justify-content-center mb-4">
#                 <div class="col-md-4">
#                     <div class="card text-white bg-primary mb-3">
#                         <div class="card-header">Balance</div>
#                         <div class="card-body">
#                             <h5 class="card-title">${{ "{:.2f}".format(current_user.balance) }}</h5>
#                         </div>
#                     </div>
#                 </div>
#                 <div class="col-md-4">
#                     <div class="card text-white bg-success mb-3">
#                         <div class="card-header">Savings</div>
#                         <div class="card-body">
#                             <h5 class="card-title">${{ "{:.2f}".format(current_user.savings) }}</h5>
#                         </div>
#                     </div>
#                 </div>
#                 <div class="col-md-4">
#                     <div class="card text-white bg-warning mb-3">
#                         <div class="card-header">Budget</div>
#                         <div class="card-body">
#                             <h5 class="card-title">${{ "{:.2f}".format(current_user.budget) }}</h5>
#                         </div>
#                     </div>
#                 </div>
#             </div>

#             <!-- Actions Section -->
#             <div class="text-center">
#                 <h4 class="mb-4">Manage Your Finances</h4>
#                 <div class="d-flex justify-content-center flex-wrap">
#                     <a href="{{ url_for('finance.deposit') }}" class="btn btn-primary m-2">Deposit</a>
#                     <a href="{{ url_for('finance.withdraw') }}" class="btn btn-danger m-2">Withdraw</a>
#                     <a href="{{ url_for('finance.save_money') }}" class="btn btn-success m-2">Save Money</a>
#                     <a href="{{ url_for('finance.withdraw_from_savings') }}" class="btn btn-info m-2">Withdraw From Savings</a>
#                 </div>
#             </div>

#         {% else %}
#             <div class="text-center">
#                 <h3>Please log in to view your account details.</h3>
#             </div>
#         {% endif %}
#     </div>
# {% endblock %}
