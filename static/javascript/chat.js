const socket = io.connect('192.168.100.4:5000/chat')
        socket.on('connect' ,(e) => { 
            
            socket.send(' connected')
        })

        document.querySelector('.bubbling').addEventListener('click' , (e) => {
            if (e.target.classList.contains('send-msg')) {
                const messageElement = e.target.previousElementSibling
                const message = messageElement.value 
                messageElement.value = ''
                const toUserName = e.target.parentElement.previousElementSibling.textContent
                socket.emit('client-sended-message',{'tousername':toUserName , 'message' : message})
                const textedTextArea = document.querySelector(`.conversationof${toUserName}`)
                textedTextArea.value = textedTextArea.value +'\n' + message
                // making all textfield to stay at bottom 
                textedTextArea.scrollTop = textedTextArea.scrollHeight


            }
            else if (e.target.classList.contains('usernametosendmessage')) {
                e.target.nextElementSibling.classList.add('display')
            }
            else if (e.target.classList.contains('goback')) {
                e.target.parentElement.classList.remove('display')
            }
        })


        // recieving messages 
        socket.on('recieved-message' , (response) => {
            // reload only if it is a new user sending message
            console.log(response['toreload'])
            if (response['toreload'] == true){
                setTimeout( () => {
                    console.log('message')
                    location.reload()
                },5000)            
            }
            else{
                const textedTextArea = document.querySelector(`.conversationof${response['fromusername']}`)
                textedTextArea.value = textedTextArea.value +'\n' + response['message']

            }
            
        })

    

        
        