
#!/bin/bash

# URL do site
URL="https://trabalho-sto-williamalencar.streamlit.app/"

while true; do
  echo "Verificando site em $(date)..."

  # Faz o request e segue redirecionamentos (-L)
  status_code=$(curl -s -o /dev/null -w "%{http_code}" -L "$URL")

  if [ "$status_code" -eq 200 ]; then
    echo "✅ Site está no ar. (Status $status_code)"
  else
    echo "❌ Site pode estar fora do ar. (Status $status_code)"
  fi

  echo "Aguardando 5 minutos..."
  sleep 300  # 5 minutos
done

