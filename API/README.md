

# Flask API

RESTful Api for pytorch models.

## **URL** : `/`

 - **Method(s)** : `GET`
 - **Example**:
 
 ```
curl  http://127.0.0.1:5000/
```
```json
   {
      "prediction": "/predict",
      "list_of_cars": "/cars"
   }
 ```

## **URL** : `/predict`

- **Method(s)** : `POST`

|Parameters  |Required  |enum	     |
|--          |--        |--      | 
| image | True |nil |
|model|True|(sfcars,indcars)

 - sfcars = stanford cars dataset model
 - indcars = indian cars model
 
```bash
curl -F 'image=@/Users/akshay/Desktop/hummer.jpg' -F 'model=sfcars'  http://127.0.0.1:5000/predict
```
```json
   {
      "predictions": [
        {
          "id": 125,
          "name": "HUMMER H3T Crew Cab 2010",
          "image": "https://carimage.netlify.app/04800.jpg"
        },
        {
          "id": 124,
          "name": "HUMMER H2 SUT Crew Cab 2009",
          "image": "https://carimage.netlify.app/06246.jpg"
        },
        [-----------] 
      ],
      "status": 200
	}
```
## **URL** : `/cars`

- **Method(s)** : `GET`
- **Parameters**:

| Parameters | Required | Enum |
|--|--|--|
| model |True  | (sfcars,indcars)
|search|False|nil
|page|False|nil

- **Response** :
```bash
curl 'http://127.0.0.1:5000/cars?model=indcars&search=maruti&page=2'
```

```json
{
  "cars": [
    {
      "id": 70,
      "name": "Maruti Suzuki Omni",
      "image": "https://carimage.netlify.app/maruti_suzuki_omni.jpg"
    },
    {
      "id": 71,
      "name": "Maruti Suzuki S-Cross",
      "image": "https://carimage.netlify.app/maruti_suzuki_s-cross.jpg"
    },
    {
      "id": 72,
      "name": "Maruti Suzuki SX4",
      "image": "https://carimage.netlify.app/maruti_suzuki_sx4.jpg"
    },
    [ --------- ]
  ],
  "status": 200
}
```

## Download Models

- Gdrive Folder Link : [DL Models](https://bit.ly/dlproject-cv)
- Download the models and copy it to `model_files` folder
