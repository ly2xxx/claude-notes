// Existing app
function fetchUsers() {
    fetch('/api/users').then(r => r.json()).then(console.log);
}