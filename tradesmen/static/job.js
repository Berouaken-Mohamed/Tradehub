function createJobCard(job) {
  const container = document.getElementById('job-container');

  const card = document.createElement('div');
  card.classList.add('job-card');

  const jobName = document.createElement('div');
  jobName.classList.add('job-name');

  const jobProfile = document.createElement('img');
  /*jobProfile.classList.add('profileImage');
  jobProfile.src = job.profileImage;*/
  jobProfile.classList.add('profile_image');
  jobProfile.src = job.profile_image;

  const jobDetail = document.createElement('div');
  jobDetail.classList.add('job-detail');

  const jobTitle = document.createElement('h3');
  jobTitle.textContent = job.title;

  const jobDescription = document.createElement('p');
  jobDescription.textContent = job.description;

  jobDetail.appendChild(jobTitle);
  jobDetail.appendChild(jobDescription);

  jobName.appendChild(jobProfile);
  jobName.appendChild(jobDetail);

  const jobLabel = document.createElement('div');
  jobLabel.classList.add('job-label');
  jobLabel.classList.add('label-a'); // Use the appropriate label class here

  const labelLink = document.createElement('a');
  labelLink.href = '#';
  labelLink.textContent = job.label; // Use the desired label text here

  jobLabel.appendChild(labelLink);

  const jobPosted = document.createElement('div');
  jobPosted.classList.add('job-posted');
  jobPosted.textContent = 'Posted ' + job.posted + ' ago';

  card.appendChild(jobName);
  card.appendChild(jobLabel);
  card.appendChild(jobPosted);

  container.appendChild(card);

  // Deleting the job
  const deleteButton = document.createElement('button');
  deleteButton.classList.add('delete-button');
  deleteButton.textContent = 'Delete';

  /*deleteButton.addEventListener('click', function () {
    // Remove the job card
    card.remove();
  });*/

  deleteButton.addEventListener('click', function () {
    // Remove the job card
    card.remove();
  
    // Make an AJAX request to delete the job from the server
    fetch('/tradesmen/delete-job/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ job_id: job.id }), // Replace 'job.id' with the actual ID of the job you want to delete
    })
      .then(response => {
        if (response.ok) {
          // Job deleted successfully
          console.log('Job deleted');
        } else {
          // Handle error response
          console.log('Error deleting job');
        }
      })
      .catch(error => {
        // Handle network or other error
        console.error('Error:', error);
      });
  });

  card.appendChild(deleteButton);
}

// Wait for the document to be ready
$(document).ready(function () {
  // Function to retrieve the CSRF token
  function getCSRFToken() {
    const cookieValue = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      .split('=')[1];
    return cookieValue;
  }

  const jobForm = document.getElementById('job-form');
  const jobContainer = document.getElementById('job-container');

  jobForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const titleInput = document.getElementById('title-input');
    const descriptionInput = document.getElementById('description-input');
    const profileImageInput = document.getElementById('profile-image-input');
    const labelInput = document.getElementById('label-input');

    const title = titleInput.value;
    const description = descriptionInput.value;
    const profileImage = profileImageInput.files[0];
    const label = labelInput.value;

    console.log('Form Data:');
    console.log('Title:', title);
    console.log('Description:', description);
    console.log('Profile Image:', profileImage);
    console.log('Label:', label);

    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('profile_image', profileImage);
    formData.append('label', label);

    // Retrieve the CSRF token
    const csrftoken = getCSRFToken();

    $.ajax({
      url: jobForm.getAttribute('data-url'),  // URL mapped to the create_job view
      type: 'POST',
      data: formData,
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      success: function (response) {
        console.log('Response:', response); // Log the response object
        // Handle the success response, e.g., show a success message

        // Append the new job to the job list section
        const newJob = response['job'];
        console.log('New Job:', newJob);
        createJobCard(newJob);

        console.log('Job created successfully');
      },
      error: function (xhr, status, error) {
        // Handle the error response, e.g., show an error message
        console.error('Error creating job:', error);
      }
    });

    // Reset the form inputs
    jobForm.reset();
  });
});

