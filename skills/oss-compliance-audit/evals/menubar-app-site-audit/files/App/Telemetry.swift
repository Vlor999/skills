import Foundation

/// Sends anonymous usage once a day to help prioritise features.
enum Telemetry {
    static let endpoint = URL(string: "https://api.volta-stats.io/v1/ping")!

    static func ping(model: String, osVersion: String, avgWatts: Double) {
        var req = URLRequest(url: endpoint)
        req.httpMethod = "POST"
        let body: [String: Any] = [
            "machineId": Host.current().localizedName ?? "unknown",
            "model": model, "os": osVersion, "avgWatts": avgWatts,
        ]
        req.httpBody = try? JSONSerialization.data(withJSONObject: body)
        URLSession.shared.dataTask(with: req).resume()
    }
}
