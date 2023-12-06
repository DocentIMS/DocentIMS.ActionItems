tinymce.PluginManager.add("DocentIMS_CreateAI", function (editor) {
  editor.ui.registry.addButton("DocentIMS_CreateAI_btn", {
    icon: "comment-add",
    onAction: () => {
      var content = editor.selection.getContent({ format: "text" });
      let tempValue = `<span style="background: yellow">${content}</span>`;
      navigator.clipboard.writeText(content).then(() => {
        if (content?.length) {
          editor.selection.setContent(tempValue);
          setTimeout(() => {
            const linkToOpen =
              "http://team.reverebeachproject.com/action-items/++add++action_items";
            window.open(linkToOpen, "_blank");
          }, 250);
        }
      });
    },
  });
});
