
    let BUTTON = document.getElementById("add-button");
    BUTTON.onclick = function addList(){          //BUTTON.addEventListener('click',function(){})
        let TEXT = document.getElementById("input-text").value;     //.value ==> text of input box
        if(!TEXT)
            alert("Input Box is Empty!");
        else{
            let ul = document.getElementById("todo-list");
            let li = document.createElement("li");
            
            li.innerHTML=TEXT;      // TEXT is available in here while declared as 'let'
            /*let t = document.createTextNode(TEXT);
            li.appendChild(t);*/    // which one is better?

            ul.appendChild(li);

            li.id = "list"+ul.childElementCount;

            let eraseButton = document.createElement("span");
            let X = document.createTextNode("x");
            eraseButton.appendChild(X);
            eraseButton.className = "close-button";

            eraseButton.id = "close-button"+ul.childElementCount;
            
            li.appendChild(eraseButton);

            
            //add event handler on clicking close button
            document.getElementById(eraseButton.id).addEventListener('click',function(){
                this.parentElement.style.display = "none";
            });
            // document.querySelect() 로 증가된 id 어떻게 접근할까?
            // 이거 두줄 쓰는데 4시간걸렸네


            //add event handler on clicking list
            document.getElementById(li.id).addEventListener('click',function(){
                this.classList.toggle("checked");
            });
        }

        document.getElementById("input-text").value = "";
        // 왜 TEXT = ""; 하면 작동 안되지?
    }

/*document.querySelector('#todo-list').addEventListener('click',function(){
    let close = document.getElementsByClassName("close-button");

    for(let i=0 ; i < close.length ; i++){
        console.log(i);
        close[i].onclick = function() {
            let li = this.parentElement;
            li.style.display = "none";
        }
    }
});*/ // 왜 이 코드는 버튼을 두번 눌러야지 없어지는걸까...