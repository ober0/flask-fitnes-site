function confirmEdit() {
    if (confirm("Вы уверены, что хотите редактировать абонемент?")) {
        document.getElementById("editForm").submit();
    }
}

function confirmDelete(id) {
    if (prompt('Введите пароль администратора') == 'adminradical'){
        window.location.href = '/delete?id=' + id
    }
    else {
        alert('Неверный пароль!')
    }
}