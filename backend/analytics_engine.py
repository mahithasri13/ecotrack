def calculate_ehi(aqi_val, potability_prob):
    """
    Calculates overall Environmental Health Index (EHI) on a 0-100 scale.
    Air Quality Weight: 50%, Water Quality Weight: 50%.
    - AQI score: 100 for AQI <= 25, scaling down to 0 for AQI >= 300.
    - Water score: Potability probability * 100.
    """
    air_score = max(0.0, min(100.0, 100.0 - (aqi_val / 3.0)))
    water_score = max(0.0, min(100.0, potability_prob * 100.0))
    
    overall_ehi = round(0.5 * air_score + 0.5 * water_score, 1)
    
    if overall_ehi >= 80:
        status = "Optimal"
        color = "emerald"
    elif overall_ehi >= 60:
        status = "Moderate"
        color = "yellow"
    elif overall_ehi >= 40:
        status = "Degraded"
        color = "orange"
    else:
        status = "Critical Risk"
        color = "red"
        
    return {
        'score': overall_ehi,
        'air_score': round(air_score, 1),
        'water_score': round(water_score, 1),
        'status': status,
        'color': color
    }

def analyze_environmental_impact(air_input=None, water_input=None, air_res=None, water_res=None):
    """
    Analyzes parameters contributing to degraded environmental quality.
    Returns impact drivers, risk scores, and domain breakdowns.
    """
    air_impacts = []
    water_impacts = []
    
    # Analyze Air Pollutants
    if air_input:
        pm25 = air_input.get('PM2.5', 0)
        pm10 = air_input.get('PM10', 0)
        no2 = air_input.get('NO2', 0)
        so2 = air_input.get('SO2', 0)
        co = air_input.get('CO', 0)
        o3 = air_input.get('O3', 0)
        
        # WHO / EPA Reference thresholds
        if pm25 > 35.4:
            air_impacts.append({'parameter': 'PM2.5', 'value': pm25, 'unit': 'µg/m³', 'severity': 'High' if pm25 > 55.4 else 'Moderate', 'impact': 'Fine particulates penetrate deep into lungs causing respiratory stress.'})
        if pm10 > 154:
            air_impacts.append({'parameter': 'PM10', 'value': pm10, 'unit': 'µg/m³', 'severity': 'High' if pm10 > 254 else 'Moderate', 'impact': 'Coarse inhalable particles affect upper respiratory tract.'})
        if no2 > 100:
            air_impacts.append({'parameter': 'NO2', 'value': no2, 'unit': 'ppb', 'severity': 'High', 'impact': 'Nitrogen Dioxide leads to airway inflammation and smog creation.'})
        if so2 > 75:
            air_impacts.append({'parameter': 'SO2', 'value': so2, 'unit': 'ppb', 'severity': 'High', 'impact': 'Sulfur Dioxide contributes to acid precipitation and pulmonary irritation.'})
        if co > 9.4:
            air_impacts.append({'parameter': 'CO', 'value': co, 'unit': 'ppm', 'severity': 'High', 'impact': 'Carbon Monoxide reduces oxygen delivery in arterial bloodstream.'})
        if o3 > 70:
            air_impacts.append({'parameter': 'O3', 'value': o3, 'unit': 'ppb', 'severity': 'Moderate', 'impact': 'Ground-level ozone damages lung tissue and vegetation.'})
            
    # Analyze Water Parameters
    if water_input:
        ph = water_input.get('ph', 7.0)
        solids = water_input.get('Solids', 0)
        sulfate = water_input.get('Sulfate', 0)
        chloramines = water_input.get('Chloramines', 0)
        thm = water_input.get('Trihalomethanes', 0)
        turbidity = water_input.get('Turbidity', 0)
        
        if ph < 6.5 or ph > 8.5:
            water_impacts.append({'parameter': 'pH', 'value': ph, 'unit': 'pH units', 'severity': 'High' if (ph < 5.5 or ph > 9.5) else 'Moderate', 'impact': f"pH of {ph} violates WHO safe drinking range (6.5 - 8.5), causing pipe corrosion or heavy metal leaching."})
        if solids > 25000:
            water_impacts.append({'parameter': 'Solids (TDS)', 'value': solids, 'unit': 'ppm', 'severity': 'Moderate', 'impact': 'High Total Dissolved Solids affect mineral taste and aquatic salinity balance.'})
        if sulfate > 350:
            water_impacts.append({'parameter': 'Sulfate', 'value': sulfate, 'unit': 'mg/L', 'severity': 'High' if sulfate > 450 else 'Moderate', 'impact': 'Excessive sulfate causes gastrointestinal discomfort and scaling in conduits.'})
        if chloramines > 8.0:
            water_impacts.append({'parameter': 'Chloramines', 'value': chloramines, 'unit': 'ppm', 'severity': 'High', 'impact': 'Elevated residual disinfectant causes eye/skin irritation and chemical odor.'})
        if thm > 80:
            water_impacts.append({'parameter': 'Trihalomethanes', 'value': thm, 'unit': 'µg/L', 'severity': 'High', 'impact': 'Disinfection byproduct linked to long-term health hazards.'})
        if turbidity > 5.0:
            water_impacts.append({'parameter': 'Turbidity', 'value': turbidity, 'unit': 'NTU', 'severity': 'High', 'impact': 'Cloudiness indicates suspended micro-particles that harbor pathogens.'})

    # Summary synthesis
    aqi_val = air_res.get('predicted_aqi', 0) if air_res else 0
    potability_prob = water_res.get('probability_potable', 1.0) if water_res else 1.0
    
    ehi = calculate_ehi(aqi_val, potability_prob)
    
    return {
        'ehi_summary': ehi,
        'air_impact_drivers': air_impacts,
        'water_impact_drivers': water_impacts,
        'total_degraded_parameters': len(air_impacts) + len(water_impacts),
        'risk_level': 'High' if (aqi_val > 150 or potability_prob < 0.4) else ('Medium' if (aqi_val > 100 or potability_prob < 0.7) else 'Low')
    }

def generate_dynamic_alerts(air_res=None, water_res=None, air_input=None, water_input=None):
    """
    Generates real-time environmental alerts based on predicted values and anomaly flags.
    """
    alerts = []
    
    if air_res:
        aqi = air_res.get('predicted_aqi', 0)
        cat = air_res.get('aqi_category', 'Good')
        is_anomaly = air_res.get('is_anomaly', False)
        reasons = air_res.get('anomaly_reasons', [])
        
        if aqi > 200:
            alerts.append({
                'title': f'Critical Air Pollution Alert (AQI {aqi})',
                'message': f'Air Quality Index is categorized as {cat}. Immediate protective measures required.',
                'category': 'Air Quality',
                'severity': 'Critical'
            })
        elif aqi > 100:
            alerts.append({
                'title': f'Air Quality Warning (AQI {aqi})',
                'message': f'Air Quality Index has reached {cat} level. Sensitive groups should restrict outdoors.',
                'category': 'Air Quality',
                'severity': 'Warning'
            })
            
        if is_anomaly:
            alerts.append({
                'title': 'Air Quality Anomaly Detected',
                'message': f"Isolation Forest flagged atypical pollutant configuration. {'; '.join(reasons) if reasons else 'Unusual atmospheric sensor drift detected.'}",
                'category': 'Air Quality',
                'severity': 'Warning' if aqi < 200 else 'Critical'
            })
            
    if water_res:
        status = water_res.get('potability_status', '')
        prob = water_res.get('probability_potable', 1.0)
        pred_class = water_res.get('predicted_class', 1)
        is_anomaly = water_res.get('is_anomaly', False)
        reasons = water_res.get('anomaly_reasons', [])
        
        if pred_class == 0:
            alerts.append({
                'title': 'Unsafe Drinking Water Alert',
                'message': f'Water sample predicted NON-POTABLE with {(1-prob)*100:.1f}% risk factor. Do not distribute without treatment.',
                'category': 'Water Quality',
                'severity': 'Critical'
            })
        elif prob < 0.7:
            alerts.append({
                'title': 'Sub-optimal Potability Warning',
                'message': f'Water sample meets basic threshold but shows reduced safety margin (Confidence: {prob*100:.1f}%).',
                'category': 'Water Quality',
                'severity': 'Warning'
            })
            
        if is_anomaly:
            alerts.append({
                'title': 'Water Quality Outlier Detected',
                'message': f"Multivariate model identified anomalous water composition. {'; '.join(reasons) if reasons else 'Unusual chemical ratio flagged.'}",
                'category': 'Water Quality',
                'severity': 'Warning'
            })
            
    if not alerts:
        alerts.append({
            'title': 'Normal Environmental Status',
            'message': 'All air quality metrics and water potability parameters remain within normal standard thresholds.',
            'category': 'System',
            'severity': 'Info'
        })
        
    return alerts

def generate_recommendations(air_res=None, water_res=None, air_input=None, water_input=None):
    """
    Provides targeted action recommendations based on predictions.
    """
    recs = []
    
    if air_res:
        aqi = air_res.get('predicted_aqi', 0)
        if aqi > 200:
            recs.append({
                'title': 'Emergency Air Action Plan',
                'recommendation': 'Deploy outdoor mask advisories (N95), mandate industrial emission curfews, and run urban misting cannons.',
                'target_domain': 'Air',
                'urgency': 'High'
            })
            recs.append({
                'title': 'Indoor Air Quality Optimization',
                'recommendation': 'Activate HEPA air purifiers indoors and close ventilation intakes facing industrial directions.',
                'target_domain': 'Air',
                'urgency': 'High'
            })
        elif aqi > 100:
            recs.append({
                'title': 'Moderate Air Quality Precaution',
                'recommendation': 'Advise schools to limit vigorous outdoor athletics during peak afternoon ozone and PM hours.',
                'target_domain': 'Air',
                'urgency': 'Medium'
            })
            
    if water_res:
        pred_class = water_res.get('predicted_class', 1)
        if pred_class == 0:
            recs.append({
                'title': 'Boil & Treat Water Protocol',
                'recommendation': 'Issue boil-water advisory for local supply and increase secondary chlorination filtration dosage at water station.',
                'target_domain': 'Water',
                'urgency': 'High'
            })
            recs.append({
                'title': 'Full Parameter Diagnostic',
                'recommendation': 'Perform immediate laboratory chromatography for Trihalomethanes and heavy metal contaminants.',
                'target_domain': 'Water',
                'urgency': 'High'
            })
        else:
            recs.append({
                'title': 'Routine System Monitoring',
                'recommendation': 'Maintain current treatment protocol and conduct scheduled weekly bio-assay checks.',
                'target_domain': 'Water',
                'urgency': 'Low'
            })

    if not recs:
        recs.append({
            'title': 'Continuous Surveillance',
            'recommendation': 'Keep automated monitoring sensors operational and ensure bi-weekly sensor calibration.',
            'target_domain': 'General',
            'urgency': 'Low'
        })
        
    return recs
