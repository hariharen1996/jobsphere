document.addEventListener('DOMContentLoaded',() => {
    setTimeout(function(){
        let message = document.querySelectorAll('.message')
        message.forEach(function(msg){
            msg.style.opacity = 0
        })
    },2000)
})