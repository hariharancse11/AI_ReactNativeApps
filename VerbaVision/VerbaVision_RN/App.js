import React, { useEffect, useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import TypeWriter from 'react-native-typewriter';

const App = () => {
  const [generatedText, setGeneratedText] = useState('');
  const [text, setText] = useState('Once upon a time');
  const [words, setWords] = useState('100');

  const handleTextChange = (text) => {
    setText(text);
  };

  const handleWordsChange = (words) => {
    setWords(words);
  };

  const generateText = () => {
    fetch(`http://34.17.22.40/generate/?text=${text}&no_of_words=${words}`)
      .then((response) => response.text())
      .then((data) => setGeneratedText(data))
      .catch((error) => console.error(error));
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Text Generator</Text>

      <TextInput
        placeholder="Enter text"
        value={text}
        onChangeText={handleTextChange}
        style={styles.textInput}
      />

      <TextInput
        placeholder="Enter word count"
        value={words}
        onChangeText={handleWordsChange}
        style={styles.textInput}
        keyboardType="numeric"
      />

      <TouchableOpacity style={styles.generateBtn} onPress={generateText}>
        <Text style={styles.generateBtnText}>Generate</Text>
      </TouchableOpacity>

      <ScrollView style={styles.generatedTextContainer}>
        <TypeWriter typing={3} style={styles.generatedText}>
          {generatedText}
        </TypeWriter>
      </ScrollView>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 30,
    paddingHorizontal: 20,
    backgroundColor: '#F5F5F5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  textInput: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    width: '100%',
    backgroundColor: '#fff',
  },
  generateBtn: {
    backgroundColor: 'skyblue',
    padding: 17,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%',
  },
  generateBtnText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  generatedTextContainer: {
    borderWidth: 2,
    borderColor: '#ccc',
    borderRadius: 10,
    marginTop: 20,
    width: '100%',
    maxHeight: 200,
    padding: 10,
    backgroundColor: '#fff',
  },
  generatedText: {
    fontSize: 16,
  },
});

export default App;
