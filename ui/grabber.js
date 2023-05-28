// Get form element and attach event listener to handle form submission
const form = document.getElementById("myForm");
const loadingAnimation = document.getElementById("loadingAnimation");
const imageContainer = document.getElementById('imageContainer');
const downloadButton = document.getElementById('downloadButton');

loadingAnimation.style.display = 'none'; // Hide loading animation initially
downloadButton.disabled = true; // Disable download button initially

form.addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent default form submission

  // Show loading animation
  loadingAnimation.style.display = "block";

  // Get input values
  const idNumber = document.getElementById("idNumberInput").value;
  const lastName = document.getElementById("lastNameInput").value;

  // Prepare URL with input values
  const url = `http://143.244.182.9:8000/get_pics/id=${idNumber}&lastName=${lastName}`;
  // Make the REST call
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
        // Handle the response data
      const imagePath = data.path;
      console.log(imagePath);
      // Generate image URLs
      const imageUrls = [];
      for (let i = 0; i <= 10; i++) {
        const imageUrl = `http://143.244.182.9/${imagePath}/image_${i.toString().padStart(1, '0')}.jpg`;
        imageUrls.push(imageUrl);
      }
       // Display the images
       imageContainer.innerHTML = '';
       imageUrls.forEach(imageUrl => {
         const imgElement = document.createElement('img');
         imgElement.src = imageUrl;
         imgElement.alt = 'Image';
         imageContainer.appendChild(imgElement);
       });
      // Enable download button
      downloadButton.disabled = false;

    })
    .catch((error) => {
      // Handle any errors
      console.error(error);
    })
    .finally(() => {
      // Hide loading animation
      loadingAnimation.style.display = "none";
    });
});

downloadButton.addEventListener('click', function() {
  // Get all images
  const images = Array.from(imageContainer.getElementsByTagName('img'));

  // Disable the download button
  downloadButton.disabled = true;

  // Create a JSZip instance
  const zip = new JSZip();

  // Keep track of downloaded images
  let downloadedCount = 0;

  // Loop through the images and add them to the zip
  images.forEach((image, index) => {
    const imageUrl = image.src;
    const fileName = `image_${index.toString().padStart(1, '0')}.jpg`;

    // Fetch the image data
    fetch(imageUrl)
      .then(response => response.blob())
      .then(blob => {
        // Add the image file to the zip
        zip.file(fileName, blob);

        // Increment the downloaded count
        downloadedCount++;

        // Check if all images have been downloaded
        if (downloadedCount === images.length) {
          // Generate the zip file
          zip.generateAsync({ type: 'blob' })
            .then(content => {
              // Create a temporary anchor element for downloading
              const downloadAnchor = document.createElement('a');
              downloadAnchor.href = URL.createObjectURL(content);
              downloadAnchor.download = 'images.zip';
              document.body.appendChild(downloadAnchor);
              downloadAnchor.click();
              document.body.removeChild(downloadAnchor);

              // Enable the download button
              downloadButton.disabled = false;
            });
        }
      })
      .catch(error => {
        console.error(error);
      });
  });
});
