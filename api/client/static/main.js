// custom javascript
let iteration = 0;
(function() {
    console.log('Sanity Check!');
  })();
  
  function handleClick(type) {
    fetch('/api/v1/tasks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ type: type }),
    })
    .then(response => response.json())
    .then(data => getStatus(data.task_id));
  }

  function createStatusCard(taskID, file_name) {
    let card = `
    <div class="card my-2" id="${taskID}" style="width: 18rem;">
      <div class="card-body" id="${taskID}-body">
        <h5 class="card-title">${file_name}</h5>
        <h6 id="${taskID}-counter" class="card-subtitle mb-2 text-muted">Processing: 0s</h6>
        <a id="${taskID}-link" href="#" class="card-link">Link Pending</a>
      </div>
    </div>
  `
  $('#task-container').prepend(card);
  }

  function createErrorStatusCard(filename, error_message) {
    let card = `
    <div class="card my-2" style="width: 18rem;">
      <div class="card-body">
        <h5 class="card-title">${filename}</h5>
        <h6 class="card-subtitle mb-2 text-danger">Failed &#x274c</h6>
        <p class="card-text">${error_message}</p>
      </div>
    </div>
  `
  $('#task-container').prepend(card);
  }

  function handleUpload() {
    let file = document.getElementById('zip_file').files[0]
    let api_key = document.getElementById('api_key').value
    let filename = file.name
    let formData = new FormData()

    if (api_key.length == 0) {
      alert("Oops! Looks like you're missing an API Key.");
      return;
    }

    formData.append("file", file)
    formData.append("api_key", api_key)

  
    if (filename.split(".").pop() === 'zip') {
      fetch('/api/v1/zip_upload/', {method: "POST", body: formData})
        .then(response => response.json())
        .then(data => {
          if (data.error != null) {
            createErrorStatusCard(filename, data.error)
          } else {
            createStatusCard(data.task_id, filename);
            getStatus(data.task_id, filename);
          }
        })
    } else {
      fetch('/api/v1/file_upload/', {method: "POST", body: formData})
        .then(response => response.json())
        .then(data => {
          if (data.error != null) {
            createErrorStatusCard(filename, data.error)
          } else {
            createStatusCard(data.task_id, filename);
            getStatus(data.task_id, filename);
          }
        })
    }
  }

  function incrementStringInt(str_number) {
    let parts = str_number.split(": ")
    return parseInt(parts[1], 10) + 1;
  }

  function updateStatusCard(taskID, response) {
    console.log(`Current Response Status: ${response.task_status}`)
    if (response.task_status === "SUCCESS") {
        console.log("Success!")

        // Update subtitle
        let counter = document.getElementById(`${taskID}-counter`)
        counter.classList.remove('text-muted')
        counter.classList.add('text-success')
        counter.innerHTML = "Complete &#x2714"

        // Update Link
        let link = document.getElementById(`${taskID}-link`)
        link.setAttribute('href', `/api/v1/results/${taskID}`)
        link.innerHTML = "Click here for results"

    } else if (response.task_status === "FAILURE") {
      console.log("Failure :(")

      // Update subtitle
      let counter = document.getElementById(`${taskID}-counter`)
      counter.classList.remove('text-muted')
      counter.classList.add('text-danger')
      counter.innerHTML = "Failed &#x274c"

      // Update Link
      let link = document.getElementById(`${taskID}-link`)
      link.remove()

      // Append error message
      let card = document.getElementById(`${taskID}-body`)
      let current_card = card.innerHTML
      let error_response = `<p class="card-text">${response.task_result}</p>`
      card.innerHTML = current_card + error_response

    } else {
      console.log("Default case!")
      let counter = document.getElementById(`${taskID}-counter`)
      let new_int = incrementStringInt(counter.innerHTML)
      counter.innerHTML = `Processing: ${new_int}s`
    } 
  }
  
  function getStatus(taskID) {
    fetch(`/api/v1/tasks/${taskID}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    })
    .then(response => response.json())
    .then(res => {
      updateStatusCard(taskID, res)
      
      const taskStatus = res.task_status;
      if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') return false;

      setTimeout(function() {
        getStatus(res.task_id);
      }, 1000);
    })
    .catch(err => console.log(err));
  }