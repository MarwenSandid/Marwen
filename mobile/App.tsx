import React, { useState } from 'react';
import { Button, Image, SafeAreaView, ScrollView, StyleSheet, Text, View } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

type CarAnalysis = {
  make: string;
  model: string;
  production_date: string;
  country_of_origin: string;
  confidence: number;
  notes: string;
};

const API_BASE_URL = 'http://10.0.2.2:8000';

export default function App() {
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [result, setResult] = useState<CarAnalysis | null>(null);
  const [loading, setLoading] = useState(false);

  const pickImage = async () => {
    const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permission.granted) return;

    const response = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 1,
    });

    if (response.canceled || !response.assets?.length) return;
    const asset = response.assets[0];
    setImageUri(asset.uri);
    setResult(null);
  };

  const analyze = async () => {
    if (!imageUri) return;
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', {
        uri: imageUri,
        name: 'car.jpg',
        type: 'image/jpeg',
      } as any);

      const res = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();
      setResult(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>Car Identifier</Text>
        <Button title="Choose Car Photo" onPress={pickImage} />

        {imageUri && <Image source={{ uri: imageUri }} style={styles.image} />}

        <View style={styles.space} />
        <Button title={loading ? 'Analyzing...' : 'Analyze Car'} onPress={analyze} disabled={!imageUri || loading} />

        {result && (
          <View style={styles.resultBox}>
            <Text>Make: {result.make}</Text>
            <Text>Model: {result.model}</Text>
            <Text>Production Date: {result.production_date}</Text>
            <Text>Country: {result.country_of_origin}</Text>
            <Text>Confidence: {result.confidence}</Text>
            <Text>Notes: {result.notes}</Text>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  content: { padding: 16, gap: 12 },
  title: { fontSize: 28, fontWeight: '700' },
  image: { width: '100%', height: 240, marginTop: 16, borderRadius: 10 },
  space: { height: 8 },
  resultBox: { marginTop: 16, padding: 12, backgroundColor: '#f3f4f6', borderRadius: 10, gap: 4 },
});
