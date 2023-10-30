tinymce.PluginManager.add("link_plugin", function (editor) {
  editor.ui.registry.addButton("link_btn", {
    icon: "duplicate",
    onAction: () => {
      var content = editor.selection.getContent({ format: "text" });
      let tempValue = `<span style="background: yellow">${content}</span>`;
      if (content?.length) editor.selection.setContent(tempValue);
    },
  });
});
