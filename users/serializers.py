from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
'''
serializers: Used for validating and transforming data in Django REST Framework.

get_user_model(): Retrieves the currently active User model (default or custom).

validate_password: Applies Django’s built-in password validation rules like minimum length, complexity, etc.
'''

User = get_user_model()
'''
This ensures that the correct User model is used based on your Django settings.
'''

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    '''
        password:
        ➤ Write-only → It won't be returned in API responses.
        ➤ Required → Must be provided.
        ➤ Validators → Uses Django’s built-in rules for password strength.

        password2:
        ➤ Acts as a confirmation password field.
        ➤ Write-only → Only used during registration requests.
    '''

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs
    '''
    attrs is the input data
    attrs is a dictionary containing all the fields provided by the user in the request. For example:

    attrs = {
        'username': 'mahesh',
        'email': 'mahesh@gmail.com',
        'password': 'abc123',
        'password2': 'abc123'
    }


    Validation logic is applied
    It checks if the password and password2 fields are equal.
    If they are not, it raises an error and the request will fail.

    Return the validated data
    If everything is fine (no errors), return attrs sends the same dictionary back so that it can be used by the create() method or further processing.
    '''

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
    
    '''
    What is validated_data here?

    After validation, suppose this is the data you receive:

    validated_data = {
        'username': 'mahesh',
        'email': 'mahesh@gmail.com',
        'password': 'abc123',
        'password2': 'abc123'
    }

    Step 1: validated_data.pop('password2')

    This line removes the password2 field because we don’t need to store it. It’s only used to check if the passwords match.

    After popping:

    validated_data = {
        'username': 'mahesh',
        'email': 'mahesh@gmail.com',
        'password': 'securepass123'
    }

    Step 2: user = User.objects.create_user(**validated_data)

    This line creates the user using Django’s built-in create_user() function.

    It's equivalent to:

    user = User.objects.create_user(
        username='mahesh',
        email='mahesh@gmail.com',
        password='abc123'
    )


    This method handles password hashing and saving the user into the database.

    Step 3: return user

    The newly created user object is returned so that the API can respond or do further processing.

    For example, you can access:

    user.id          # unique user ID
    user.username    # 'mahesh'
    user.email       # 'mahesh@gmail.com'

    '''
