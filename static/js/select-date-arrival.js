function submitDate() {
    var anyDateCheckbox = document.getElementById('anyDate');
    var selectedDate = document.getElementById('datepicker').value;

    if (anyDateCheckbox.checked || selectedDate !== '') {
        document.getElementById("dateForm").submit();
    } else {
        alert('Пожалуйста, выберите дату или установите флажок "Любая дата".');
    }
}

document.getElementById('anyDate').addEventListener('change', function() {
    var dateInput = document.getElementById('dateInput');
    if (this.checked) {
        dateInput.style.display = 'none';
    } else {
        dateInput.style.display = 'block';
    }
});