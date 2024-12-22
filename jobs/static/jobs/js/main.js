document.addEventListener('DOMContentLoaded',() => {
    setTimeout(function(){
        const alert = document.querySelectorAll('.alert')
        alert.forEach(function(alerts){
            alerts.style.display = 'none'
        })
    },2000)
})