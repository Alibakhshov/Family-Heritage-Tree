function validateForm() {
    var bio = document.getElementById("bio").value;
    var birthDate = document.getElementById("birth_date").value;
    var age = document.getElementById("age").value;
    var phone = document.getElementById("phone").value;
    var address = document.getElementById("address").value;

    var bioError = document.getElementById("bioError");
    var birthDateError = document.getElementById("birthDateError");
    var ageError = document.getElementById("ageError");
    var phoneError = document.getElementById("phoneError");
    var addressError = document.getElementById("addressError");

    bioError.innerHTML = "";
    birthDateError.innerHTML = "";
    ageError.innerHTML = "";
    phoneError.innerHTML = "";
    addressError.innerHTML = "";

    var isValid = true;

    if (bio === "") {
        bioError.innerHTML = "Bio is required";
        isValid = false;
    }

    if (birthDate === "") {
        birthDateError.innerHTML = "Date of Birth is required";
        isValid = false;
    }

    if (age === "") {
        ageError.innerHTML = "Age is required";
        isValid = false;
    }

    if (phone === "") {
        phoneError.innerHTML = "Phone is required";
        isValid = false;
    }

    if (address === "") {
        addressError.innerHTML = "Address is required";
        isValid = false;
    }

    if (isValid) {
        document.getElementById("profileFormInfo").submit();
    }
}
