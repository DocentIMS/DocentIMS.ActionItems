tinymce.PluginManager.add("DocentIMS_CreateAI", function (editor) {
  editor.ui.registry.addButton("DocentIMS_CreateAI_btn", {
    icon: "comment-add",
    onAction: () => {
      const body = document.body;
      var content = editor.selection.getContent({ format: 'text' });
      var baseUrl = body.getAttribute('data-base-url');
      var portalUrl = body.getAttribute('data-portal-url');
      var to_uuid = "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c => (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16));
      let tempValue = `<a href="a href="../resolveuid/${to_uuid}"><span style="background: yellow">${content}</span></a>`;
      // console.log(tempValue);
      navigator.clipboard.writeText(content).then(() => {
        if (content?.length) {
          
          editor.selection.setContent(tempValue);
          setTimeout(() => {
            // Variable replacement did not work
            const linkToOpen = portalUrl +'/action-items/++add++action_items?from_url=' + baseUrl + '&to_uuid=' + to_uuid;
            window.open(linkToOpen, "_blank");
          }, 250);
        }
      });
    },
  });
});
