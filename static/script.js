function showEditButtons(container, show=true){
    let id = container.id.split('-')[1];
    let edit_buttons = document.querySelector("#edit-buttons-"+id);

    if(show === false){
        edit_buttons.style.visibility = "hidden";
        container.style.backgroundColor = "transparent";
    }else{
        edit_buttons.style.visibility = "visible";
        container.style.backgroundColor = "#E0e0e0";
        
    };
};

function pressTab(button){
    button.style.backgroundColor = "rgb(200, 41, 34)";
    button.style.cursor = "default";
    if(button.id === "actionable"){
        let x = document.querySelector('#non-actionable');
        x.style.backgroundColor = "#e4433a";
        x.style.cursor = "pointer";
    }else{
        let x = document.querySelector('#actionable');
        x.style.backgroundColor = "#e4433a";
        x.style.cursor = "pointer";
    };
};

function pressSearchTab(button){
    pressTab(button);
    let list_1 = document.getElementById('actionable-list');
    let list_2 = document.getElementById('non-actionable-list');
    if(button.id === "actionable"){
        list_1.style.display = "block";
        list_2.style.display = "none";
    }else{
        list_1.style.display = "none";
        list_2.style.display = "block";
    };
};

function initializeTab(seeingActionables){
    console.log(seeingActionables)
    if(seeingActionables === "True"){
        let x = document.querySelector('#actionable');
        x.style.backgroundColor = "rgb(200, 41, 34)";
        x.style.cursor = "default";

    }else{
        let x = document.querySelector('#non-actionable');
        x.style.backgroundColor = "rgb(200, 41, 34)";
        x.style.cursor = "default";
    };
};