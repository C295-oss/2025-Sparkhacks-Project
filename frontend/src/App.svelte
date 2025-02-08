<script>
  import { writable } from 'svelte/store';
	import Modal from 'svelte-simple-modal';
  import Popup from './Popup.svelte';
  const modal = writable(null);
  const showModal = () => modal.set(Popup);

  let text_to_generate;
  let html_from_fastapi;
  let template_num = -1;
  
  async function start_parseLang()
  {
    console.log(text_to_generate)

    if (!text_to_generate) {
        return;
    }

    let url = `http://127.0.0.1:8000/visualize/${encodeURIComponent(text_to_generate)}`;

    const response = await fetch(url);
    const data = await response.text();

    console.log(data);
  }

  window.onbeforeunload = function() {
        fetch("http://127.0.0.1:8000/shutdown", { method: "POST" });
  };

  // async function get_html() {
  //   let url = "http://127.0.0.1:8000/getHTML";

  //   try {
  //       const response = await fetch(url);
  //       if (!response.ok) {
  //           throw new Error(`HTTP error! Status: ${response.status}`);
  //       }
  //       const data = await response.text();
  //       console.log("Received HTML:", data);
  //   } catch (error) {
  //       console.error("Fetch error:", error);
  //   }
  // }

  async function load_template() {
    let url = `http://127.0.0.1:8000/template/${encodeURIComponent(template_num)}`;

    const response = await fetch(url);
    const data = await response.text()

    console.log(data)




  }

</script>

<main id="main_window">

  <h1>GenWeb</h1>

  <p>Create your first webpage here. Once you're finished, press 'GENERATE'. We'll take care of the rest.</p>

  <Modal show={$modal}>
    <button on:click={showModal}>Show modal</button>
  </Modal>

  <div>
    <button id="templates_btn">Templates</button>
    <button id="visual" on:click={start_parseLang}>Display</button>
    <button id="pdf_btn">Generate PDF</button>
    <button id="html_btn">Generate HTML</button> <!--on:click={get_html}-->
    <button id="generate_btn" >Generate Project</button>
  </div>

  <textarea id="code_gen" bind:value={text_to_generate}></textarea>

</main>

<style>

main {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
  justify-content: center;
}

textarea {
  width: 100%;
  height: 70%;
  margin-bottom: 10px;  
  height: 90vh;
  padding: 10px;
}

button {
  margin-bottom: 10px;
}

</style>
