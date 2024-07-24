import { View, Text, ScrollView, Alert } from 'react-native'
import { Link, router } from 'expo-router'
import { SafeAreaView } from 'react-native-safe-area-context'
import {React, useState} from 'react'
import CustomButton from '../../components/CustomButton' 
import FormInput from '../../components/FormInput'
import GoogleAuth from '../../components/GoogleAuth'
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_ENDPOINT = 'http://127.0.0.1:8000/api/login/'

const SignIn = () => {

  const handleLogin = async () => {
    if (!form.email || !form.password){
      Alert.alert('Error', 'Please fill in all the fields')
      return;
    }

    try {

      const response = await axios.post(API_ENDPOINT, {
        email: form.email, 
        password: form.password
      });

      if (response.status === 200){
        const {access, refresh} = response.data; 
        await AsyncStorage.setItem('access', access); 
        await AsyncStorage.setItem('refresh', refresh);
        Alert.alert('Success', 'Login successful');
        form.email = '';
        form.password = '';
        router.replace('/home');
      }

    } catch(error){
      const errorMessage = error.response?.data?.detail || 'Login failed';
      Alert.alert('Error', JSON.stringify(errorMessage));
    }
  }

  const [form, setForm] = useState({
    email: '', 
    password: ''
  })


  return (
    <SafeAreaView className="bg-white h-full">
      <ScrollView>

        <View className="items-center">
          <FormInput 
            title="Email"
            value = {form.email}
            otherStyles = "mt-8"
            handleChangeText = {(e) => {setForm({...form, email: e})}}
            keyboardType = "email-address"
          />
          <FormInput 
            title="Password"
            otherStyles = "mt-8"
            value = {form.password}
            handleChangeText = {(e) => {setForm({...form, password: e})}}
          
          /> 
          <CustomButton 
            title="Sign In"
            containerStyles="w-[85vw] mt-8"
            handlePress = {handleLogin}
          />

          <Link className="mt-4" href="/">Forgot Password?</Link>
        </View>

        <View className="mt-8 ml-4">
          <Text>Don't Have an Acccount? {' '}
          <Link
             href="/sign-up"
             className="text-lg font-semibold"
             >
              Sign Up
            </Link>

            {' '} or
          </Text>
          <GoogleAuth />
        </View>
        


      </ScrollView>
    </SafeAreaView>
  )
}

export default SignIn