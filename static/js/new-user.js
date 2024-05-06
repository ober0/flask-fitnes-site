function confirmEdit() {
    var error = false
    if (document.getElementById('subscription_number').value == ''){
        error = true;
        document.getElementById('subscription_number').style.border = '3px solid red'
    }
    else {
        document.getElementById('subscription_number').style.border = '1px solid white'
    }
    if (document.getElementById('name').value == ''){
        error = true;
        document.getElementById('name').style.border = '3px solid red'
    }
    else {
        document.getElementById('name').style.border = '1px solid white'
    }
    if (document.getElementById('date_signing').value == ''){
        error = true;
        document.getElementById('date_signing').style.border = '3px solid red'
    }
    else {
        document.getElementById('date_signing').style.border = '1px solid white'
    }

    if (!error){
        if (confirm("Вы уверены, что хотите добавить абонемент?")) {
            document.getElementById("editForm").submit();
        }
    }
    else {
        alert('Введите обязательные значения!')
    }

}