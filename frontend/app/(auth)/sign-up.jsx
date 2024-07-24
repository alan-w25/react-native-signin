import { View, Text, ScrollView, Alert} from 'react-native'
import { Link,router } from 'expo-router'
import { SafeAreaView } from 'react-native-safe-area-context'
import {React, useState} from 'react'
import CustomButton from '../../components/CustomButton' 
import FormInput from '../../components/FormInput'
import GoogleAuth from '../../components/GoogleAuth'
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/register/'

const SignUp = () => {

  const [form, setForm] = useState({
    email: '', 
    password: '',
    password2:'',
    username:''
  })

  const handleRegister = async () => {
    if (!form.username || !form.email || !form.password || !form.password2){
      Alert.alert('Error', 'Please fill in all the fields')

    }

    if (form.password !== form.password2) {
      Alert.alert('Error', 'Passwords do not match')
      return;
    }

    try {
      const response = await axios.post(API_URL, {
        email:form.email,
        username:form.username, 
        password:form.password,
        password2:form.password2
      }); 

      if (response.status === 201){
        Alert.alert('Success', "Registration successful")
        form.email = ''
        form.username = ''
        form.password = ''
        form.password2 = ''
        router.replace('/sign-in')
      }
    } catch (error) {
      const errorMessage = error.response?.data || 'Registration failed';
      console.log(errorMessage); // Log the detailed error message
      Alert.alert('Error', JSON.stringify(errorMessage));
    }
  }




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
            title="Username"
            otherStyles = "mt-8"
            value = {form.username}
            handleChangeText = {(e) => {setForm({...form, username: e})}}
          
          /> 
          <FormInput 
            title="Password"
            otherStyles = "mt-8"
            value = {form.password}
            handleChangeText = {(e) => {setForm({...form, password: e})}}
          
          /> 
          <FormInput 
            title=""
            placeholder = "confirm password"
            value = {form.password2}
            handleChangeText = {(e) => {setForm({...form, password2: e})}}
          
          /> 
          <CustomButton 
            title="Sign Up"
            containerStyles="w-5/6 mt-8"
            handlePress = {handleRegister}
          />
        </View>

        <View className="mt-8 ml-4">
          <Text>Already have an account? {' '}
          <Link
             href="/sign-in"
             className="text-lg font-semibold"
             >
              Sign In
            </Link>

            {' '} or
          </Text>
          <GoogleAuth />
        </View>
        


      </ScrollView>
    </SafeAreaView>
  )
}

export default SignUp