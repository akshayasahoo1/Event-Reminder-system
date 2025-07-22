function validateForm() {
    let name = document.getElementById('name').value;
    let date = document.getElementById('date').value;
    let time = document.getElementById('time').value;
    
    if (!name || !date || !time) {
        alert('Please fill in all required fields.');
        return false;
    }
    
    let today = new Date().toISOString().split('T')[0];
    if (date < today) {
        alert('Event date cannot be in the past.');
        return false;
    }
    
    return true;
}
