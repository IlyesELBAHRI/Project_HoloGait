Shader "Custom/Water" {
    Properties {
        _MainTex ("Main Texture", 2D) = "white" {}
        _Speed ("Speed", Range(0, 10)) = 1
    }
 
    SubShader {
        Tags {"Queue"="Transparent" "RenderType"="Transparent"}
        LOD 200
 
        CGPROGRAM
        #pragma surface surf Lambert alpha
 
        sampler2D _MainTex;
        float _Speed;
 
        struct Input {
            float2 uv_MainTex;
        };
 
        void surf (Input IN, inout SurfaceOutput o) {
            float2 uv = IN.uv_MainTex * _Speed + _Time.y;
            float2 distortion = tex2D(_MainTex, uv).rg * 0.1;
            uv += distortion;
 
            o.Alpha = 0.5; // Réglez la transparence de l'eau ici
            o.Albedo = tex2D(_MainTex, uv).rgb;
        }
        ENDCG
    }
    FallBack "Diffuse"
}
