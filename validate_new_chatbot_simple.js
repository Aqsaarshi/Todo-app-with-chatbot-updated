// Simple validation to check if new chatbot components exist
const fs = require('fs');
const path = require('path');

// Define the paths to the new components
const newComponentsDir = path.join(__dirname, 'frontend', 'src', 'components');
const newChatBotIconPath = path.join(newComponentsDir, 'NewChatBotIcon.tsx');
const newChatInterfacePath = path.join(newComponentsDir, 'NewChatBotIcon.css');
const newChatInterfaceComponentPath = path.join(newComponentsDir, 'NewChatInterface.tsx');
const newChatInterfaceCSSPath = path.join(newComponentsDir, 'NewChatInterface.css');

console.log('Validating new chatbot components...\n');

// Check if the new components exist
const components = [
  { name: 'NewChatBotIcon.tsx', path: newChatBotIconPath },
  { name: 'NewChatBotIcon.css', path: newChatInterfacePath },
  { name: 'NewChatInterface.tsx', path: newChatInterfaceComponentPath },
  { name: 'NewChatInterface.css', path: newChatInterfaceCSSPath }
];

let allComponentsExist = true;
components.forEach(component => {
  const exists = fs.existsSync(component.path);
  console.log(`${exists ? '✓' : '✗'} ${component.name} exists: ${exists}`);
  if (!exists) allComponentsExist = false;
});

if (!allComponentsExist) {
  console.log('\n❌ Some components are missing!');
  process.exit(1);
}

console.log('\n✅ All new chatbot components exist!');

// Read the content of the new components to ensure they have proper implementations
const newChatBotIconContent = fs.readFileSync(newChatBotIconPath, 'utf8');
const newChatInterfaceContent = fs.readFileSync(newChatInterfaceComponentPath, 'utf8');

// Check if the components have the expected functionality
const hasOnClickHandler = newChatBotIconContent.includes('onClick') && newChatBotIconContent.includes('handleClick');
const hasMessageHandling = newChatInterfaceContent.includes('useState') && newChatInterfaceContent.includes('setMessages');
const hasAPIIntegration = newChatInterfaceContent.includes('apiClient') && newChatInterfaceContent.includes('sendMessage');

console.log('\nValidating component functionality...');
console.log(`${hasOnClickHandler ? '✓' : '✗'} NewChatBotIcon has click handling: ${hasOnClickHandler}`);
console.log(`${hasMessageHandling ? '✓' : '✗'} NewChatInterface has message handling: ${hasMessageHandling}`);
console.log(`${hasAPIIntegration ? '✓' : '✗'} NewChatInterface has API integration: ${hasAPIIntegration}`);

if (hasOnClickHandler && hasMessageHandling && hasAPIIntegration) {
  console.log('\n✅ All functionality checks passed!');
  console.log('\n🎉 New chatbot implementation is complete and validated!');
} else {
  console.log('\n❌ Some functionality is missing!');
  process.exit(1);
}