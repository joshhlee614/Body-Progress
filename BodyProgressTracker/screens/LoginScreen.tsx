import React, { useState } from 'react'
import { View, Text, StyleSheet } from 'react-native'
import TextInput from '../components/TextInput'
import Button from '../components/Button'
import type { NativeStackNavigationProp } from '@react-navigation/native-stack'

type RootStackParamList = {
  Home: undefined
  'Upload Photo': undefined
  'Progress Graph': undefined
  Settings: undefined
  Login: undefined
}

type LoginScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Login'>
}

const BACKEND_URL = 'http://10.0.0.114:8000'

export default function LoginScreen({ navigation }: LoginScreenProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleLogin = async () => {
    if (loading) return
    setLoading(true)
    setError('')
    try {
      const res = await fetch(`${BACKEND_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      if (!res.ok) {
        const data = await res.json()
        setError(data.detail || 'login failed')
        setLoading(false)
        return
      }
      // login success
      setLoading(false)
      navigation.replace('Home')
    } catch (e) {
      setError('network error')
      setLoading(false)
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>login</Text>
      <TextInput
        value={email}
        onChangeText={setEmail}
        placeholder="email"
        autoCapitalize="none"
      />
      <TextInput
        value={password}
        onChangeText={setPassword}
        placeholder="password"
        autoCapitalize="none"
        secureTextEntry
      />
      {error ? <Text style={styles.error}>{error}</Text> : null}
      <Button title={loading ? 'logging in...' : 'login'} onPress={handleLogin} />
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24
  },
  title: {
    fontSize: 24,
    marginBottom: 24
  },
  error: {
    color: 'red',
    marginVertical: 8
  }
}) 