tinymce.PluginManager.add("DocentIMS_CreateAI", function (editor) {
  editor.ui.registry.addButton("DocentIMS_CreateAI_btn", {
    icon: "comment-add",
    onAction: () => {
      const body = document.body;
      var content = editor.selection.getContent({ format: 'text' });
      const baseUrl = body.getAttribute('data-base-url');
      let tempValue = '<a href="${baseUrl}"><span style="background: yellow">${content}</span></a>';
      alert(content);
      alert(baseUrl);
      alert(tempValue);
      navigator.clipboard.writeText(content).then(() => {
        if (content?.length) {
          editor.selection.setContent(tempValue);
          setTimeout(() => {
            const linkToOpen = "${baseUrl}/action-items/++add++action_items";
            window.open(linkToOpen, "_blank");
          }, 250);
        }
      });
    },
  });
});
