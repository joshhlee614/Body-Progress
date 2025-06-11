import React from 'react'
import { TouchableOpacity, Text, StyleSheet } from 'react-native'

type ButtonProps = {
  title: string
  onPress: () => void
}

export default function Button({ title, onPress }: ButtonProps) {
  return (
    <TouchableOpacity style={styles.btn} onPress={onPress}>
      <Text style={styles.text}>{title}</Text>
    </TouchableOpacity>
  )
}

const styles = StyleSheet.create({
  btn: {
    backgroundColor: '#222',
    padding: 12,
    borderRadius: 6,
    alignItems: 'center',
    marginVertical: 6,
  },
  text: {
    color: '#fff',
    fontSize: 16,
  },
}) 