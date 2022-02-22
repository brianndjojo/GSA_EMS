
const dataString = document.getElementById('users_list').innerText
/*https://stackoverflow.com/questions/42494823/json-parse-returns-string-instead-of-object*/
const data = JSON.parse(dataString);
const data2 = JSON.parse(data)

const searchForm = document.getElementById('search-user')
const searchInput = document.getElementById('search-user-input')
const resultsBox = document.getElementById('user-list')

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value



retrievedElements = resultsBox.getElementsByTagName('a')
let filteredUsers = []

searchInput.addEventListener('keyup', e=>{
  console.log(e.target.value) 
  
  filteredUsers = data2.filter(
    info => info['username'].includes(e.target.value)
  );

  

  $(".user-output").each(function() {
    $(this).addClass("hide");
    username = $(this).children("div").children('.usernames')[0].innerText
    
    if(filteredUsers.length > 0){
    
      for(i = 0; i < filteredUsers.length; i++){
        if(filteredUsers[i]['username'] == username){
          $(this).removeClass("hide")
        }
      }
     

    }

  });
})
 


 

