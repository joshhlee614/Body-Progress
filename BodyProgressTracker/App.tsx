/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 */

import * as React from 'react'
import { NavigationContainer } from '@react-navigation/native'
import { createNativeStackNavigator } from '@react-navigation/native-stack'
import { View, Text } from 'react-native'
import type { NativeStackNavigationProp } from '@react-navigation/native-stack'

const Stack = createNativeStackNavigator()

type RootStackParamList = {
  Home: undefined
  'Upload Photo': undefined
  'Progress Graph': undefined
  Settings: undefined
}

function HomeScreen({ navigation }: { navigation: NativeStackNavigationProp<RootStackParamList, 'Home'> }) {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>home screen</Text>
      <Text style={{ margin: 8 }} onPress={() => navigation.navigate('Upload Photo')}>go to upload photo</Text>
      <Text style={{ margin: 8 }} onPress={() => navigation.navigate('Progress Graph')}>go to progress graph</Text>
      <Text style={{ margin: 8 }} onPress={() => navigation.navigate('Settings')}>go to settings</Text>
    </View>
  )
}

function UploadPhotoScreen() {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>upload photo screen</Text>
    </View>
  )
}

function ProgressGraphScreen() {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>progress graph screen</Text>
    </View>
  )
}

function SettingsScreen() {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>settings screen</Text>
    </View>
  )
}

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Upload Photo" component={UploadPhotoScreen} />
        <Stack.Screen name="Progress Graph" component={ProgressGraphScreen} />
        <Stack.Screen name="Settings" component={SettingsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  )
}
