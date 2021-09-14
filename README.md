# Stats NFT ERC721 Contract Showcase

Pseudo-random token ID. For more information visit official [website](https://stattz.github.io/).

## Deployment

We use google functions to dynamically create SVG images and metadata JSON.

```
gcloud functions deploy metadata --runtime python39 --trigger-http
gcloud functions deploy image --runtime python39 --trigger-http
```

## Info

```
gcloud functions describe metadata    
```

## Logging

```
gcloud functions logs read metadata
```

## Clean Up

```
gcloud functions delete metadata
gcloud functions delete image
```

## Endpoints

```
https://us-central1-universal-stats-326006.cloudfunctions.net/metadata?tokenId=0x9ebd75abc7359c0b9f407ffcbf7a58b977562f882a8ae72ec96ae76c01e77c23
https://us-central1-universal-stats-326006.cloudfunctions.net/image?tokenId=0x9ebd75abc7359c0b9f407ffcbf7a58b977562f882a8ae72ec96ae76c01e77c23
```
