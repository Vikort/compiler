document doc = new document('doc.xml');
node someNode = new node('tag');
attribute someAtr = new attribute('atrName');
someNode = ‘content’;
someAtr = ‘value’;

doc = ‘newDoc.xml’; // this is a comment and this line override path to xml doc
doc.save();
node rootNode = doc.root(); 
node[] foundedNode = doc.findNode(‘content’);


node[] tempNode = someNode.findNode(‘content’);


attribute[] nodeAtrs = someNode.attribute;
someNode += someAtr;
someNode += ‘+ new content’;
node firstNode = someNode[0];

someNode(2) = ‘new content’; //override content of text node from 2 pos (string starts with 0 pos)

someNode(2) += ‘+ new content’; //add content to text node from 2 pos

someNode.insert(0,newTag); //insert node to 0 pos

someNode.add(newText); //insert node to the end of nodes

print(someNode);
del(someNode);
del(someAtr);
doc.delete();

if (someNode == ‘content’) { 
   someNode = ‘newContent’;
   print(someNode);
} else { 
   print(someNode);
}

for(node i in root){
  print(i);
} 

current = doc.root();

while (current.size()){
   print(current); 
   current = current[0];
}

node someFunc(node someNode){
   print(someNode);
}

doc = (document) node


