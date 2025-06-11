import React from 'react'
import { TextInput as RNTextInput, StyleSheet } from 'react-native'

type Props = {
  value: string
  onChangeText: (text: string) => void
  placeholder?: string
}

export default function TextInput({ value, onChangeText, placeholder }: Props) {
  return (
    <RNTextInput
      style={styles.input}
      value={value}
      onChangeText={onChangeText}
      placeholder={placeholder}
      placeholderTextColor="#888"
    />
  )
}

const styles = StyleSheet.create({
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 6,
    padding: 10,
    fontSize: 16,
    marginVertical: 6,
    backgroundColor: '#fff',
  },
}) 