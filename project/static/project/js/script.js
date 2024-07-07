var showchat = document.querySelector('.show-chatbot');
var closechat = document.querySelector('.close-chat');
var chatbot = document.querySelector('.chatbot');
var form = document.querySelector('.chat-type');
var input = document.querySelector('.chat-input');
var chatting = document.querySelector('.chatting');
var button = document.querySelector('.Submit');
var submit_button = document.querySelector('.submit-button');

showchat.addEventListener('click',()=>{
    chatbot.style.display = 'block';
})

closechat.addEventListener('click',()=>{
    chatbot.style.display='none';
})

function SubmitForm(event){
    event.preventDefault();
    const input_value = input.value;

    if (input_value.trim() === ''){
        return;
    }

    // to add the user message
    const usermessage = document.createElement('div');
    usermessage.classList.add('user');

    const innerusermessage = document.createElement('div');
    innerusermessage.classList.add('right');

    const userheading = document.createElement('p');
    userheading.textContent = 'User:';
    userheading.classList.add('user-written');

    const innerusermessagecontent = document.createElement('p');
    innerusermessagecontent.textContent = input_value;

    innerusermessage.appendChild(innerusermessagecontent);
    usermessage.appendChild(userheading);
    usermessage.appendChild(innerusermessage);
    chatting.appendChild(usermessage);    
    input.value = '';
    scrolltobottom();

    // to add the bot message
    const botmessage = document.createElement('div');
    botmessage.classList.add('bot');

    const innerbotmessage = document.createElement('div');
    innerbotmessage.classList.add('left');

    const botheading = document.createElement('p');
    botheading.textContent = 'Bot:';
    botheading.classList.add('bot-written');

    const innerbotmessagecontent = document.createElement('p');
    innerbotmessagecontent.textContent = 'Thinking...';

    innerbotmessage.appendChild(innerbotmessagecontent);
    botmessage.appendChild(botheading);
    botmessage.appendChild(innerbotmessage);
    chatting.appendChild(botmessage);  
    scrolltobottom();
    button.setAttribute('disabled','disabled');
    submit_button.style.color = 'gray';

    fetch(`/result/${input_value}`,{
        method: 'POST',
        headers: { 
            "Content-type": "application/x-www-form-urlencoded",
            'X-CSRFToken':getCookie('csrftoken')
        },
        body: `message=${input_value}`
    }).then((response) =>{
        console.log('response',response);
        return response.json()
    }).then((data) =>{
        console.log('data',data);
        const botmessage = data.response;
        // change the bot default message with the model response
        innerbotmessagecontent.textContent = botmessage;
        innerbotmessage.classList.add('left-success-color');
        scrolltobottom();
        button.removeAttribute('disabled');
        submit_button.style.color = 'white';
    }).catch((error)=>{
        const errormessage = 'Result does not get fetched';
        innerbotmessagecontent.textContent = errormessage;
        innerbotmessage.classList.add('left-error-color');
        button.removeAttribute('disabled');
        submit_button.style.color = 'white';
    })

    // to pass the django csrf protection during post request
    function getCookie(name){
        let cookievalue = null;
        if (document.cookie && document.cookie!==''){
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0,name.length+1) ===(name + '=')) {
                    cookievalue = decodeURIComponent(cookie.substring(name.length+1));
                    break;
                }
            }
        }
        return cookievalue
    }

    // scroll to bottom whenever a new message comes
    function scrolltobottom(){
        chatting.scrollTop = chatting.scrollHeight;
    }
}

form.addEventListener('submit',SubmitForm);